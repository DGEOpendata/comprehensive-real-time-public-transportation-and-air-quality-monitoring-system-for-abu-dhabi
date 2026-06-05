python
import requests
import pandas as pd
import folium

def fetch_transportation_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Error fetching transportation data.")

def fetch_air_quality_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Error fetching air quality data.")

def create_map(transportation_data, air_quality_data):
    city_map = folium.Map(location=[24.466667, 54.366669], zoom_start=12)

    for route in transportation_data['routes']:
        for stop in route['stops']:
            folium.Marker(
                location=[stop['latitude'], stop['longitude']],
                popup=f"Stop: {stop['name']}\nRoute: {route['route_name']}\nFrequency: {route['frequency']} mins",
                icon=folium.Icon(color='blue', icon='bus', prefix='fa')
            ).add_to(city_map)

    for station in air_quality_data['stations']:
        folium.CircleMarker(
            location=[station['latitude'], station['longitude']],
            radius=7,
            color='green' if station['AQI'] <= 50 else 'red',
            fill=True,
            fill_color='green' if station['AQI'] <= 50 else 'red',
            popup=f"Station: {station['name']}\nAQI: {station['AQI']}\nPM2.5: {station['PM2.5']} µg/m³\nPM10: {station['PM10']} µg/m³"
        ).add_to(city_map)

    return city_map

# Example API URLs for data
transportation_api_url = "https://api.example.com/abu-dhabi-transportation"
air_quality_api_url = "https://api.example.com/abu-dhabi-air-quality"

# Fetch and process data
transportation_data = fetch_transportation_data(transportation_api_url)
air_quality_data = fetch_air_quality_data(air_quality_api_url)

# Generate map
city_map = create_map(transportation_data, air_quality_data)

# Save map as an HTML file
city_map.save("abu_dhabi_transport_air_quality_map.html")
