# Satellite Tracking and Pass Prediction Dashboard

A web-based satellite tracking dashboard that retrieves orbital data from CelesTrak, propagates satellite orbits using SGP4 and predicts upcoming satellite passes over a selected ground station.

The project was developed as part of the **ROSPIN Summer School**.

ROSPIN – Romanian Space Initiative:
https://github.com/Romanian-Space-Initiative

## Features

* Retrieve up-to-date TLE orbital data from CelesTrak
* Local TLE caching
* Support for multiple satellites
* SGP4 orbit propagation using Skyfield
* Current satellite position
* Latitude, longitude and altitude
* Satellite velocity
* Ground-track prediction
* Interactive world map
* Custom ground-station location
* Upcoming satellite-pass prediction
* Rise, culmination and set times
* Maximum elevation prediction
* Azimuth calculation
* Automatic dashboard refresh

## Technologies

* Python
* Skyfield
* SGP4
* Streamlit
* Folium
* Streamlit-Folium
* Pandas
* Requests
* CelesTrak orbital data

## Project Structure

```text
Rospin-project/
│
├── app.py
├── main.py
├── map_view.py
├── ui.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── tle_service.py
│   ├── orbit.py
│   ├── ground_station.py
│   └── passes.py
│
└── data/
    └── cache/
        └── tle_cache.json
```

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd satellite-tracking-dashboard
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

## Running the Dashboard

Start the Streamlit application with:

```bash
streamlit run app.py
```

Streamlit will display a local address, usually:

```text
http://localhost:8501
```

Open it in a web browser.

## How It Works

The application follows the following processing pipeline:

```text
CelesTrak
    ↓
TLE data
    ↓
TLE Service
    ↓
Skyfield / SGP4
    ↓
Orbit Propagation
    ↓
Current Position + Ground Track
    ↓
Ground Station
    ↓
Pass Prediction
    ↓
Streamlit Dashboard
```

### TLE Data

The application retrieves Two-Line Element data from CelesTrak.

The TLE module handles:

* downloading orbital data;
* parsing TLE records;
* validating the data;
* caching TLEs locally;
* using cached data if the remote service is temporarily unavailable.

### Orbit Propagation

The TLE data is converted into a Skyfield `EarthSatellite` object.

SGP4 propagation is then used to calculate:

* current latitude;
* current longitude;
* altitude;
* velocity;
* future satellite positions;
* ground track.

### Ground Station

By default, the application uses Cluj-Napoca as the ground station.

The user can modify:

* station name;
* latitude;
* longitude;
* altitude.

### Pass Prediction

The application predicts upcoming satellite passes above the selected ground station.

For each pass, it can calculate:

* rise time;
* maximum elevation time;
* set time;
* maximum elevation;
* azimuth;
* distance.

## Example Satellites

The application currently supports satellites such as:

* ISS (ZARYA)
* Sentinel-1A
* Sentinel-2A
* Sentinel-2B

Additional satellites can easily be added to the satellite configuration.

## Future Development

Possible future improvements include:

* support for larger satellite fleets;
* multiple ground stations;
* user accounts;
* pass notifications;
* contact scheduling;
* API access;
* ground-station hardware integration;
* antenna pointing commands;
* imaging opportunity prediction;
* target-area visibility prediction.

The imaging opportunity feature could allow a user to select a geographic area and determine when an Earth observation satellite is able to observe that location.

## Startup Potential

The project could evolve into a satellite mission planning platform for universities, CubeSat teams, ground-station operators and Earth observation users.

A commercial version could offer automatic pass scheduling, notifications, multi-ground-station support, fleet management and API integrations.

