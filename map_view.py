import folium
from folium import plugins

def create_map(satellite_pos, ground_station_pos, ground_track_coords):
    """
    Creează o hartă Folium cu satelitul, stația la sol și ground track.
    """
    # Centrăm harta pe poziția satelitului și dezactivăm repetiția hărții (world wrap)
    m = folium.Map(
        location=[satellite_pos['latitude'], satellite_pos['longitude']],
        zoom_start=2,
        no_wrap=True,
        max_bounds=True
    )
    
    # Adăugăm Ground Track (gestionând trecerile peste antimeridian)
    if ground_track_coords:
        segments = []
        current_segment = []
        
        for i in range(len(ground_track_coords)):
            point = ground_track_coords[i]
            coord = (point['latitude'], point['longitude'])
            
            if not current_segment:
                current_segment.append(coord)
            else:
                prev_lon = current_segment[-1][1]
                curr_lon = coord[1]
                
                # Dacă diferența de longitudine este foarte mare (> 180), înseamnă că am trecut peste antimeridian
                if abs(curr_lon - prev_lon) > 180:
                    segments.append(current_segment)
                    current_segment = [coord]
                else:
                    current_segment.append(coord)
        
        if current_segment:
            segments.append(current_segment)
            
        for segment in segments:
            folium.PolyLine(
                locations=segment,
                color='blue',
                weight=2,
                opacity=0.7,
                tooltip='Ground Track'
            ).add_to(m)
        
    # Marker Stație la Sol
    folium.Marker(
        location=[ground_station_pos['lat'], ground_station_pos['lon']],
        popup=f"Ground Station: {ground_station_pos['name']}",
        icon=folium.Icon(color='green', icon='home')
    ).add_to(m)
    
    # Marker Satelit
    folium.Marker(
        location=[satellite_pos['latitude'], satellite_pos['longitude']],
        popup=f"Satellite: {satellite_pos['name']}",
        icon=folium.Icon(color='red', icon='record', prefix='fa')
    ).add_to(m)
    
    return m
