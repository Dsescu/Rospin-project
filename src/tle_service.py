import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

CELESTRAK_URL = "https://celestrak.org/NORAD/elements/gp.php"

# CelesTrak data is normally updated about every 2 hours.
CACHE_DURATION = timedelta(hours=2)

CACHE_FILE = Path("data/cache/tle_cache.json")

SATELLITES = {
    "ISS": {
        "query_type": "CATNR",
        "value": "25544",
        "expected_name": "ISS (ZARYA)"
    },

    "SENTINEL-1A": {
        "query_type": "NAME",
        "value": "SENTINEL-1A",
        "expected_name": "SENTINEL-1A"
    },

    "SENTINEL-2A": {
        "query_type": "NAME",
        "value": "SENTINEL-2A",
        "expected_name": "SENTINEL-2A"
    },

    "SENTINEL-2B": {
        "query_type": "NAME",
        "value": "SENTINEL-2B",
        "expected_name": "SENTINEL-2B"
    }
}

def parse_tle(text):
    """
    Convert the raw TLE response received from CelesTrak
    into a list of dictionaries.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        raise ValueError("No TLE data found in response.")

    # A TLE response with satellite names contains:
    # name
    # line 1
    # line 2
    if len(lines) % 3 != 0:
        raise ValueError("TLE data is not in the expected format (3 lines per satellite).")

    satellites = []

    for i in range(0, len(lines), 3):
        name = lines[i]
        line1 = lines[i + 1]
        line2 = lines[i + 2]

        if not line1.startswith("1 "):
            raise ValueError(
                f"Invalid TLE line 1 for satellite {name}"
            )

        if not line2.startswith("2 "):
            raise ValueError(
                f"Invalid TLE line 2 for satellite {name}"
            )

        # NORAD catalog number is present in both TLE lines
        norad_line1 = line1[2:7].strip()
        norad_line2 = line2[2:7].strip()

        if norad_line1 != norad_line2:
            raise ValueError(
                f"NORAD catalog numbers do not match for {name}"
            )

        satellites.append({
            "name": name,
            "norad_catalog_number": norad_line1,
            "line1": line1,
            "line2": line2
        })

    return satellites

def download_tle(query_type, value):
    """
    Download TLE data from CelesTrak.

    query_type can be:
    CATNR
    NAME
    GROUP
    """

    params = {
        query_type: value,
        "FORMAT": "TLE"
    }

    headers = {
        "User-Agent": "TLE Service/1.0"
    }

    response = requests.get(
        CELESTRAK_URL,
        params=params,
        headers=headers,
        timeout=10,
        allow_redirects=False
    )

    if response.status_code != 200:
        raise requests.HTTPError(
            f"Failed to download TLE data: {response.status_code} {response.reason}"
        )
    return parse_tle(response.text)

def load_cache():
    """
    Load previously downloaded TLE data.
    """

    if not CACHE_FILE.exists():
        return {}

    try:
        with open(CACHE_FILE,"r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}

def save_cache(data):
    """
    Save TLE data locally.
    """
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def cache_is_valid(cache_entry):
    """
    Check if the cache entry is still valid.
    """

    if not cache_entry:
        return False

    downloaded_at = cache_entry.get("downloaded_at")
    if not downloaded_at:
        return False

    try:
        downloaded_time = datetime.fromisoformat(downloaded_at)
    except ValueError:
        return False

    current_time = datetime.now(timezone.utc)
    return current_time - downloaded_time < CACHE_DURATION

def select_satellite(results, expected_name):
    """
    Select the wanted satellite from a CelesTrak response.

    NAME queries can theoretically return more than one satellite,
    so we search for an exact name match.
    """

    for satellite in results:

        if satellite["name"].upper() == expected_name.upper():
            return satellite

    # If only one result exists, use it.
    if len(results) == 1:
        return results[0]

    raise ValueError(
        f"Satellite '{expected_name}' was not found in the response."
    )

def get_satellite_tle(satellite_key, force_refresh=False):
    """
    Main function used by the rest of the application.

    It first checks the cache.
    If the cache is older than 2 hours, it downloads fresh data.
    If CelesTrak is unavailable, it falls back to old cached data.
    """

    satellite_key = satellite_key.upper()
    if satellite_key not in SATELLITES:
        raise ValueError(f"Satellite '{satellite_key}' is not supported.")

    config = SATELLITES[satellite_key]

    cache = load_cache()
    cache_entry = cache.get(satellite_key)

    # Use fresh cached data
    if (
        not force_refresh
        and cache_is_valid(cache_entry)
    ):
        satellite = cache_entry["tle"].copy()
        satellite["source"] = "cache"

        return satellite

    try:
        results = download_tle(
            config["query_type"],
            config["value"]
        )

        satellite = select_satellite(
            results,
            config["expected_name"]
        )

        cache[satellite_key] = {
            "downloaded_at": datetime.now(timezone.utc).isoformat(),
            "tle": satellite
        }

        save_cache(cache)

        satellite = satellite.copy()
        satellite["source"] = "CelesTrak"

        return satellite

    except (requests.RequestException, ValueError) as error:
        if cache_entry:

            print(
                f"Warning: CelesTrak unavailable: {error}"
            )

            print(
                "Using older cached TLE data."
            )

            satellite = cache_entry["tle"].copy()
            satellite["source"] = "old cache"

            return satellite

        raise

def get_available_satellites():
    """
    Return the list of satellites configured in the application.
    """

    return list(SATELLITES.keys())
