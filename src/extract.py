import requests
import pandas as pd
import geopandas as gpd
from datetime       import datetime, timedelta

def extract_boundaries(geojson_path: str = "data/ken_admin_boundaries.geojson"):
    # Download zip manually first, unzip, load
    gdf = gpd.read_file(geojson_path)
    nakuru = gdf[gdf['ADM1_EN'] == 'Nakuru']  # or filter ADM1_PCODE == 'KE032'
    nakuru.to_file("data/nakuru_boundary.geojson", driver="GeoJSON")
    return nakuru

def extract_weather(start_date: str = "2020-01-01", end_date: str = None):
    if not end_date:
        end_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")  # account for delay
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude=-0.72&longitude=36.43&start_date={start_date}&end_date={end_date}"
        f"&daily=rain_sum,temperature_2m_mean&timezone=Africa/Nairobi"
    )
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame({
        'date': pd.to_datetime(data['daily']['time']),
        'rain_sum_mm': data['daily']['rain_sum'],
        'temp_mean_c': data['daily']['temperature_2m_mean']
    })
    df.to_parquet("data/weather_raw.parquet")
    return df

def extract_agri_csv(csv_path: str = "data/nakuru_maize.csv"):  # Manually create from KNBS report / KilimoSTAT download
    # Columns: year, county, maize_area_ha, maize_production_mt, yield_mt_ha
    df = pd.read_csv(csv_path)
    df.to_parquet("data/agri_raw.parquet")
    return df