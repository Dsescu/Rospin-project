from skyfield.api import wgs84


DEFAULT_LATITUDE = 46.7712
DEFAULT_LONGITUDE = 23.6236
DEFAULT_ELEVATION_M = 0


def get_ground_station(
    latitude=DEFAULT_LATITUDE,
    longitude=DEFAULT_LONGITUDE,
    elevation_m=DEFAULT_ELEVATION_M
):

    return wgs84.latlon(latitude, longitude, elevation_m)