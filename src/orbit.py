from datetime import timedelta

from skyfield.api import EarthSatellite, load


ts = load.timescale()


def create_satellite(tle):
    """
    creeaza un obiect Skyfield EarthSatellite din datele TLE.
    """

    satellite = EarthSatellite(
        tle["line1"],
        tle["line2"],
        tle["name"],
        ts
    )

    return satellite


def get_position_at_time(satellite, time):
    """
    calculeaza pozitia satelitului la un anumit moment.
      return in latitude, longitude si altitude in kilometri.
    """

    geocentric = satellite.at(time)
    subpoint = geocentric.subpoint()

    return {
        "latitude": float(subpoint.latitude.degrees),
        "longitude": float(subpoint.longitude.degrees),
        "altitude_km": float(subpoint.elevation.km)
    }


def get_current_position(satellite):
    """
    calculeaza pozitia curenta a satelitului.
    """

    current_time = ts.now()

    return get_position_at_time(
        satellite,
        current_time
    )


def generate_ground_track(satellite, minutes=90, step_seconds=60):
    """
    genereaza ground track-ul satelitului pentru o perioada de timp.
    fiecare pozitie contine:
        - time
        - latitude
        - longitude
        - altitude_km
    """

    start_time = ts.now()

    positions = []

    number_of_points = int((minutes * 60) / step_seconds) + 1

    for i in range(number_of_points):
        time = ts.utc(
            start_time.utc_datetime() +
            timedelta(seconds=i * step_seconds)
        )

        position = get_position_at_time(
            satellite,
            time
        )

        position["time"] = time.utc_iso()

        positions.append(position)

    return positions