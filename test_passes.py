from src.tle_service import get_satellite_tle
from src.orbit import create_satellite, ts
from src.ground_station import get_ground_station
from src.passes import get_next_passes

tle = get_satellite_tle("ISS")
satellite = create_satellite(tle)

ground_station = get_ground_station()

print("Satellite:", tle["name"])
print("Ground station: Cluj-Napoca\n")

passes = get_next_passes(
    satellite,
    ground_station,
    ts,
    hours=24,
    min_elevation_deg=10
)

print(f"Found {len(passes)} pass(es) in the next 24 hours:\n")

for i, p in enumerate(passes, start=1):
    print(f"Pass {i}:")
    print(f"  Rise:  {p['rise']}  (azimuth {p['rise_azimuth_deg']:.1f}°)")
    print(f"  Max:   {p['max_time']}  (elevation {p['max_elevation_deg']:.1f}°, azimuth {p['max_azimuth_deg']:.1f}°)")
    print(f"  Set:   {p['set']}  (azimuth {p['set_azimuth_deg']:.1f}°)")
    print()

print("\n--- Verificare filtrare ---\n")

for threshold in [10, 30, 50]:
    filtered = get_next_passes(
        satellite,
        ground_station,
        ts,
        hours=24,
        min_elevation_deg=threshold,
        max_passes=10
    )
    elevations = [p["max_elevation_deg"] for p in filtered]

    print(f"min_elevation_deg={threshold}: {len(filtered)} treceri, elevatii maxime: {[round(e, 1) for e in elevations]}")

    assert all(e >= threshold for e in elevations), (
        f"Eroare: o trecere cu elevatie sub {threshold}° a trecut de filtru!"
    )

print("\nToate verificarile au trecut.")