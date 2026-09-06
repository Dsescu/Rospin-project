from datetime import timedelta
from skyfield.api import wgs84

from src.ground_station import get_ground_station


def get_altaz(satellite, ground_station, time):

    difference = satellite - ground_station
    topocentric = difference.at(time)
    altitude, azimuth, distance = topocentric.altaz()
    return {
        "elevation_deg": float(altitude.degrees),
        "azimuth_deg": float(azimuth.degrees),
        "distance_km": float(distance.km)
    }


def get_next_passes(
    satellite,
    ground_station,
    ts,
    start_time=None,
    hours=24,
    min_elevation_deg=10,
    max_passes=10
):

    if start_time is None:
        start_time = ts.now()
    end_time = ts.utc(start_time.utc_datetime() + timedelta(hours=hours))

    times, events = satellite.find_events(
        ground_station,
        start_time,
        end_time,
        altitude_degrees=min_elevation_deg
    )

    passes = []
    current_pass = {}

    for time, event in zip(times, events):
        altaz = get_altaz(satellite, ground_station, time)

        if event == 0:
            current_pass = {
                "rise": time.utc_iso(),
                "rise_azimuth_deg": altaz["azimuth_deg"]
            }
        elif event == 1:
            current_pass["max_time"] = time.utc_iso()
            current_pass["max_elevation_deg"] = altaz["elevation_deg"]
            current_pass["max_azimuth_deg"] = altaz["azimuth_deg"]
        elif event == 2:
            current_pass["set"] = time.utc_iso()
            current_pass["set_azimuth_deg"] = altaz["azimuth_deg"]
            passes.append(current_pass)
            current_pass = {}

    return passes[:max_passes]