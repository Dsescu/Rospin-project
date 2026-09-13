import streamlit as st
from streamlit_folium import st_folium
import time
from datetime import datetime

from src.tle_service import get_satellite_tle
from src.orbit import create_satellite, get_current_position, generate_ground_track, ts
from src.ground_station import get_ground_station
from src.passes import get_next_passes
from ui import render_sidebar, display_info_cards, display_passes_table
from map_view import create_map

st.set_page_config(page_title="Satellite Tracker Dashboard", layout="wide")

def main():
    # 1. Render Sidebar si preluare configuratii
    config = render_sidebar()
    
    st.title(f"🛰️ Satellite Tracking: {config['satellite']}")
    
    # 2. Incarcare Date Satelit (TLE)
    # Folosim numele pentru a căuta TLE-ul. În tle_service.py, get_satellite_tle primește un satellite_key.
    # Presupunem că satellite_key poate fi numele.
    try:
        tle_data = get_satellite_tle(config['satellite'])
        satellite = create_satellite(tle_data)
    except Exception as e:
        st.error(f"Error loading TLE for {config['satellite']}: {e}")
        return

    # 3. Calculare Pozitie Curenta si Ground Track
    current_pos = get_current_position(satellite)
    current_pos['name'] = config['satellite']
    ground_track = generate_ground_track(satellite, minutes=90, step_seconds=60)
    
    # 4. Configurare Ground Station
    gs_obj = get_ground_station(config['gs_lat'], config['gs_lon'], config['gs_alt'])
    gs_info = {
        'name': config['gs_name'],
        'lat': config['gs_lat'],
        'lon': config['gs_lon']
    }
    
    # 5. Calculare Treceri Viitoare
    upcoming_passes = get_next_passes(satellite, gs_obj, ts)
    
    # 6. Afisare Info Cards
    display_info_cards(current_pos)
    
    # 7. Afisare Harta
    st.subheader("Live Map & Ground Track")
    folium_map = create_map(current_pos, gs_info, ground_track)
    st_folium(folium_map, width=None, height=500, returned_objects=[])
    
    # 8. Afisare Tabel Treceri
    display_passes_table(upcoming_passes)
    
    # 9. Refresh Automat
    # Streamlit poate face auto-refresh folosind st.empty() si un loop, 
    # sau mai elegant cu st.rerun() declanșat de un timer (experimental_rerun a devenit rerun).
    # Pentru a nu bloca interfata, folosim un mic hack cu time.sleep si rerun.
    
    time.sleep(config['refresh_rate'])
    st.rerun()

if __name__ == "__main__":
    main()
