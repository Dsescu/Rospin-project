from src.tle_service import get_satellite_tle
from src.orbit import (
    create_satellite,
    get_current_position,
    generate_ground_track
)

tle = get_satellite_tle("ISS")

# obiectul satelitului
satellite = create_satellite(tle)

# pozitia curenta
position = get_current_position(satellite)

print("Satellite:", tle["name"])
print("Current position:")
print("Latitude:", position["latitude"])
print("Longitude:", position["longitude"])
print("Altitude:", position["altitude_km"], "km")

track = generate_ground_track(
    satellite,
    minutes=90,
    step_seconds=60
)

print("Ground track points:", len(track))
print("First point:", track[0])
print("Last point:", track[-1])
