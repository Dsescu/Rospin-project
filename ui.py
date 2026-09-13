import streamlit as st
import pandas as pd
from src.tle_service import get_available_satellites

def render_sidebar():
    st.sidebar.title("Satellite Tracker Settings")
    
    # Selector Satelit
    sat_options = get_available_satellites()
    selected_sat = st.sidebar.selectbox("Select Satellite", sat_options)
    
    st.sidebar.divider()
    
    # Input Ground Station
    st.sidebar.subheader("Ground Station Settings")
    gs_name = st.sidebar.text_input("Station Name", value="Cluj-Napoca")
    gs_lat = st.sidebar.number_input("Latitude", value=46.7712, format="%.4f")
    gs_lon = st.sidebar.number_input("Longitude", value=23.6236, format="%.4f")
    gs_alt = st.sidebar.number_input("Elevation (m)", value=0)
    
    st.sidebar.divider()
    
    # Auto-refresh interval
    refresh_rate = st.sidebar.slider("Refresh rate (seconds)", 5, 60, 10)
    
    return {
        "satellite": selected_sat,
        "gs_name": gs_name,
        "gs_lat": gs_lat,
        "gs_lon": gs_lon,
        "gs_alt": gs_alt,
        "refresh_rate": refresh_rate
    }

def display_info_cards(sat_data):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Altitude", f"{sat_data['altitude_km']:.2f} km")
    col2.metric("Latitude", f"{sat_data['latitude']:.4f}°")
    col3.metric("Longitude", f"{sat_data['longitude']:.4f}°")
    col4.metric("Velocity", f"{sat_data['velocity_km_s']:.2f} km/s") 
    
def display_passes_table(passes):
    st.subheader("Upcoming Passes")
    if not passes:
        st.write("No upcoming passes found in the next 24h.")
        return

    df = pd.DataFrame(passes)
    # Redenumire coloane pentru aspect mai frumos
    df_display = df.rename(columns={
        "rise": "Rise Time (UTC)",
        "max_time": "Max Elevation Time (UTC)",
        "max_elevation_deg": "Max Elevation (°)",
        "set": "Set Time (UTC)"
    })
    
    # Adăugăm informația despre următoarea trecere vizibil
    next_pass = passes[0]
    st.info(f"**Next Pass:** {next_pass['max_time']} (Max Elevation: {next_pass['max_elevation_deg']:.2f}°)")
    
    # Selectăm doar câteva coloane relevante dacă sunt prea multe
    cols = ["Rise Time (UTC)", "Max Elevation Time (UTC)", "Max Elevation (°)"]
    st.table(df_display[cols])
