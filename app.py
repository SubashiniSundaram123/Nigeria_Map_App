
import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import re

st.set_page_config(layout="wide")
st.title("🗺️ Map of Mineral Titles with Tooltips and Google Maps Links")


# --- Coordinate Parsing ---
def dms_to_dd(deg, minutes, seconds, direction):
    dd = float(deg) + float(minutes) / 60 + float(seconds) / 3600
    if direction.upper() in ['S', 'W']:
        dd *= -1
    return dd


def parse_coordinates(coord_str):
    if pd.isna(coord_str):
        return np.nan, np.nan

    coord_str = coord_str.replace(',', ' ').replace('&', ' ')
    coord_str = coord_str.replace('o', '°').replace('’', "'").replace('”', '"')
    coord_str = coord_str.upper()

    # Try DMS like "4 52 15E, 6 53 45N"
    try:
        pattern = re.findall(r'(\d+)\s+(\d+)\s+(\d+)\s*([NSEW])', coord_str)
        if len(pattern) >= 2:
            lon = dms_to_dd(*pattern[0])
            lat = dms_to_dd(*pattern[1])
            return lat, lon
    except:
        pass

    # Try full fancy DMS like 'N 07° 24' 41.5" E 005° 14' 32.2"'
    try:
        pattern = re.findall(
            r'([NS])\s*(\d+)[°O]?\s*(\d+)[\'′]\s*([\d.]+)["”]?\s*([EW])\s*(\d+)[°O]?\s*(\d+)[\'′]\s*([\d.]+)["”]?',
            coord_str)
        if pattern:
            lat_d, lat_m, lat_s = pattern[0][1], pattern[0][2], pattern[0][3]
            lon_d, lon_m, lon_s = pattern[0][5], pattern[0][6], pattern[0][7]
            lat = dms_to_dd(lat_d, lat_m, lat_s, pattern[0][0])
            lon = dms_to_dd(lon_d, lon_m, lon_s, pattern[0][4])
            return lat, lon
    except:
        pass

    return np.nan, np.nan


# --- Load Excel from Local Path (instead of file uploader) ---
local_excel_path = "data/Active _Operational Mineral Tiles.xlsx"  # 👉 Update this path as needed

try:
    df = pd.read_excel(local_excel_path)
    st.success("✅ File loaded successfully from local path.")
except Exception as e:
    st.error(f"❌ Failed to load file. Error: {e}")
    st.stop()

# --- Coordinate Processing ---
coord_col = "GEOGRAPHICAL COORDINATES OF THE MINERAL TITLE ( LONG. & LAT)"
if coord_col not in df.columns:
    st.error(f"Column '{coord_col}' not found in Excel file.")
    st.stop()

df["Latitude"], df["Longitude"] = zip(*df[coord_col].apply(parse_coordinates))
valid_coords = df.dropna(subset=["Latitude", "Longitude"]).copy()

if valid_coords.empty:
    st.warning("⚠️ No valid coordinates found.")
    st.dataframe(df)
    st.stop()

# --- Add Google Maps Link ---
valid_coords["📍 Coordinates"] = valid_coords.apply(
    lambda row: f'<a href="https://www.google.com/maps?q={row["Latitude"]},{row["Longitude"]}" target="_blank">📍 View on Map</a>',
    axis=1
)

# --- Search Filter ---
search_text = st.text_input("🔍 Search by Title, State, or anything:")
if search_text:
    filtered_df = valid_coords[valid_coords.apply(lambda row: search_text.lower() in str(row).lower(), axis=1)]
else:
    filtered_df = valid_coords

# --- Show Table with Links ---
st.markdown("### 📄 Mineral Titles Table (with Google Maps Link)")
st.write(filtered_df.to_html(escape=False, index=False), unsafe_allow_html=True)

# --- Map Visualization ---
st.markdown("### 🗺️ Map View")
m = folium.Map(location=[filtered_df["Latitude"].mean(), filtered_df["Longitude"].mean()], zoom_start=8,
               control_scale=True)
marker_cluster = MarkerCluster().add_to(m)

# --- Color by Activity ---
color_palette = ['red', 'green', 'blue', 'purple', 'orange', 'darkred', 'lightgray']
category_column = "ACTIVITY" if "ACTIVITY" in filtered_df.columns else None
unique_categories = filtered_df[category_column].unique().tolist() if category_column else []
category_color_map = {cat: color_palette[i % len(color_palette)] for i, cat in enumerate(unique_categories)}

for _, row in filtered_df.iterrows():
    lat, lon = row["Latitude"], row["Longitude"]
    title = row.get("TITLE", "No Title")
    state = row.get("STATE", "")
    activity = row.get(category_column, "Other") if category_column else "Other"
    color = category_color_map.get(activity, "gray")

    popup_text = f"<b>{title}</b><br>State: {state}<br>Activity: {activity}"
    folium.Marker(
        location=[lat, lon],
        popup=popup_text,
        tooltip=title,
        icon=folium.Icon(color=color, icon="info-sign")
    ).add_to(marker_cluster)

st_folium(m, width=1200, height=1000)
