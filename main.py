from src.tle_service import (
    get_available_satellites,
    get_satellite_tle
)


print("Available satellites:")

for satellite_name in get_available_satellites():
    print("-", satellite_name)


print("\nDownloading ISS TLE...\n")

iss = get_satellite_tle("ISS")


print("Satellite:", iss["name"])
print("NORAD ID:", iss["norad_catalog_number"])
print("Source:", iss["source"])

print("\nTLE:")

print(iss["line1"])
print(iss["line2"])