import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import re
import io

st.set_page_config(layout="wide")
st.title("🗺️ Nigeria Mineral Titles Explorer")


# --- Coordinate Parsing ---
def dms_to_dd(deg, minutes, seconds, direction):
    dd = float(deg) + float(minutes) / 60 + float(seconds) / 3600
    return -dd if direction.upper() in ['S', 'W'] else dd


def parse_coordinates(coord_str):
    if pd.isna(coord_str):
        return np.nan, np.nan

    coord_str = coord_str.replace(',', ' ').replace('&', ' ')
    # Use simple character replacements for degree, minute, second symbols
    coord_str = coord_str.replace('o', '°')
    # Replace any single quote variants with standard single quote
    for char in ["'", "′", "'"]:
        coord_str = coord_str.replace(char, "'")
    # Replace any double quote variants with standard double quote
    for char in ['"', '"', '"']:
        coord_str = coord_str.replace(char, '"')

    coord_str = coord_str.upper()

    try:
        pattern = re.findall(r'(\d+)\s+(\d+)\s+(\d+)\s*([NSEW])', coord_str)
        if len(pattern) >= 2:
            lon = dms_to_dd(*pattern[0])
            lat = dms_to_dd(*pattern[1])
            return lat, lon
    except:
        pass

    try:
        pattern = re.findall(
            r'([NS])\s*(\d+)[°O]?\s*(\d+)[\'′]\s*([\d.]+)[""]?\s*([EW])\s*(\d+)[°O]?\s*(\d+)[\'′]\s*([\d.]+)[""]?',
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


# --- Load Excel ---
file_path = "data/Nigeria Licenced Mine Inventory.xlsx"
try:
    df = pd.read_excel(file_path)
    st.success("✅ Data loaded successfully.")
except Exception as e:
    st.error(f"❌ Failed to load file: {e}")
    st.stop()

# --- Parse Coordinates ---
coord_col = "GEOGRAPHICAL COORDINATES OF THE MINERAL TITLE ( LONG. & LAT)"
if coord_col not in df.columns:
    st.error(f"Column '{coord_col}' not found.")
    st.stop()

df["Latitude"], df["Longitude"] = zip(*df[coord_col].apply(parse_coordinates))
valid_coords = df.dropna(subset=["Latitude", "Longitude"]).copy()

if valid_coords.empty:
    st.warning("⚠️ No valid coordinates found.")
    st.dataframe(df)
    st.stop()

# --- Google Maps Links ---
valid_coords["📍 Coordinates"] = valid_coords.apply(
    lambda
        row: f'<a href="https://www.google.com/maps?q={row["Latitude"]},{row["Longitude"]}" target="_blank">📍 View</a>',
    axis=1
)

# --- Search ---
search_text = st.text_input("🔍 Search by Title, State, or Activity:")
if search_text:
    filtered_df = valid_coords[valid_coords.apply(lambda row: search_text.lower() in str(row).lower(), axis=1)]
else:
    filtered_df = valid_coords

# --- MAP FIRST ---
st.markdown("### 🌍 Map View of Titles")

# Create map with Google Maps hybrid satellite imagery (with labels)
tiles_url = "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"
m = folium.Map(
    location=[9.0820, 8.6753],  # Centered on Nigeria
    zoom_start=6,
    control_scale=True,
    tiles=tiles_url,
    attr="Google Hybrid Satellite"
)

marker_cluster = MarkerCluster().add_to(m)

# --- Color by Activity ---
# Use two prominent colors like in the reference image (blue and orange)
color_palette = ['#1E88E5', '#FF8F00']  # Blue and orange similar to the reference image

# Determine which field to use for coloring (ACTIVITY, MINERAL, STATUS are good candidates)
# You can change this to any column you want to distinguish between different types of markers
color_category_col = "ACTIVITY" if "ACTIVITY" in filtered_df.columns else "MINERAL" if "MINERAL" in filtered_df.columns else "STATUS"

if color_category_col in filtered_df.columns:
    categories = filtered_df[color_category_col].unique().tolist()
    # Simplify categories to just use two main colors (blue and orange)
    # Assign first half to blue, second half to orange for visual distinction
    half_idx = len(categories) // 2
    color_map = {}
    for i, cat in enumerate(categories):
        if i < half_idx:
            color_map[cat] = color_palette[0]  # Blue
        else:
            color_map[cat] = color_palette[1]  # Orange
else:
    color_map = {"Default": color_palette[0]}

# Create a legend for the map
legend_html = '''
<div style="position: fixed;
     bottom: 50px; right: 50px; width: 200px; height: auto;
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; padding: 10px; border-radius: 5px;">
     <div style="font-weight:bold; margin-bottom:5px;">Legend</div>
'''
if color_category_col in filtered_df.columns:
    for cat, color in color_map.items():
        legend_html += f'<div><span style="background-color:{color}; width:15px; height:15px; display:inline-block; margin-right:5px; border-radius:50%;"></span>{cat}</div>'
legend_html += '</div>'
m.get_root().html.add_child(folium.Element(legend_html))

# Create separate marker clusters for blue and orange markers
blue_cluster = MarkerCluster(name="Blue Markers").add_to(m)
orange_cluster = MarkerCluster(name="Orange Markers").add_to(m)

# Add markers with detailed information from table
for _, row in filtered_df.iterrows():
    lat, lon = row["Latitude"], row["Longitude"]

    # Extract all available columns to create a detailed popup
    popup_html = "<div style='max-width:300px;'>"

    # Get company name/title holder for both popup and tooltip
    # We'll first try the exact column "NAME OF COMPANY/ MINERAL TITLE HOLDER"
    company_name = row.get('NAME OF COMPANY/ MINERAL TITLE HOLDER', '')
    # Fallback to other similar columns if the specific one doesn't exist
    if not company_name:
        company_name = row.get('COMPANY NAME', '') or row.get('NAME OF COMPANY', '') or row.get('MINERAL TITLE HOLDER',
                                                                                                '')

    # Use company name as the popup header instead of "No Title"
    popup_html += f"<h4 style='margin:0;padding-bottom:5px;border-bottom:1px solid #ccc;'>{company_name}</h4>"

    # Prominently display location/state information if available
    if 'STATE' in row and not pd.isna(row['STATE']):
        popup_html += f"<div style='font-weight:bold;font-size:14px;margin:5px 0;background:#f0f0f0;padding:3px;'>STATE: {row['STATE']}</div>"

    # Include key information fields (except STATE which is already shown above)
    key_fields = ["ACTIVITY", "MINERAL", "STATUS"]
    for field in key_fields:
        if field in row and not pd.isna(row[field]):
            details_html += f"<b>{field}:</b> {row[field]}<br>"

    # Add "View More Details" as a expandable section
    popup_html += "<div style='margin-top:10px;'><details>"
    popup_html += "<summary style='color:#1E88E5;cursor:pointer;'>View More Details</summary>"

    # Add content to the details section
    details_html = "<div style='margin-top:5px;padding-top:5px;'>"

    # Add remaining fields that aren't already shown
    excluded_fields = key_fields + ["Latitude", "Longitude", coord_col, "📍 Coordinates", "COMPANY NAME",
                                    "NAME OF COMPANY", "MINERAL TITLE HOLDER", "NAME OF COMPANY/ MINERAL TITLE HOLDER",
                                    "STATE"]
    for col in row.index:
        if col not in excluded_fields and not pd.isna(row[col]):
            details_html += f"<b>{col}:</b> {row[col]}<br>"

    details_html += "</div>"
    popup_html += details_html
    popup_html += "</details></div>"

    # Add Google Maps link
    popup_html += f"<div style='margin-top:10px;'><a href='https://www.google.com/maps?q={lat},{lon}' target='_blank' style='color:#E91E63;text-decoration:none;display:flex;align-items:center;'><span style='font-size:16px;margin-right:5px;'>📍</span> View in Google Maps</a></div>"
    popup_html += "</div>"

    # Determine marker color based on category
    if color_category_col in row and not pd.isna(row[color_category_col]):
        category = row[color_category_col]
        marker_color = color_map.get(category, color_palette[0])
    else:
        marker_color = color_palette[0]  # Default to blue

    # Create tooltip with company name as primary information
    # First check specifically for "NAME OF COMPANY/ MINERAL TITLE HOLDER" column
    tooltip = row.get("NAME OF COMPANY/ MINERAL TITLE HOLDER", "")
    # If empty, use fallback label
    if not tooltip:
        tooltip = company_name if company_name else "Unknown Company"

    # Add mineral information if available
    if 'MINERAL' in row and not pd.isna(row['MINERAL']):
        tooltip += f" ({row['MINERAL']})"

    # Create circle marker for a more modern look similar to the reference image
    marker = folium.CircleMarker(
        location=[lat, lon],
        radius=8,
        popup=folium.Popup(popup_html, max_width=350),
        tooltip=tooltip,
        color=marker_color,
        fill=True,
        fill_color=marker_color,
        fill_opacity=0.7,
        weight=2
    )

    # Add to appropriate cluster based on color
    if marker_color == color_palette[0]:  # Blue
        marker.add_to(blue_cluster)
    else:  # Orange
        marker.add_to(orange_cluster)

# Add layer control to toggle between marker groups
folium.LayerControl().add_to(m)

st_folium(m, width=1200, height=700)

# --- TABLE SECOND ---
st.markdown("### 📋 Titles Table with Google Maps Links")
st.write(filtered_df.to_html(escape=False, index=False), unsafe_allow_html=True)

# --- DOWNLOAD BUTTONS ---
st.markdown("### 📥 Download Filtered Data")

# CSV
csv_data = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download CSV",
    data=csv_data,
    file_name="filtered_titles.csv",
    mime="text/csv"
)

# Excel
excel_buffer = io.BytesIO()
with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
    filtered_df.to_excel(writer, index=False, sheet_name="Titles")
excel_data = excel_buffer.getvalue()
st.download_button(
    label="⬇️ Download Excel",
    data=excel_data,
    file_name="filtered_titles.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# import streamlit as st
# import pandas as pd
# import numpy as np
# import folium
# from folium.plugins import MarkerCluster
# from streamlit_folium import st_folium
# import re
# import io

# st.set_page_config(layout="wide")
# st.title("🗺️ Nigeria Mineral Titles Explorer")

# # --- Coordinate Parsing ---
# def dms_to_dd(deg, minutes, seconds, direction):
#     dd = float(deg) + float(minutes) / 60 + float(seconds) / 3600
#     return -dd if direction.upper() in ['S', 'W'] else dd

# def parse_coordinates(coord_str):
#     if pd.isna(coord_str):
#         return np.nan, np.nan

#     coord_str = coord_str.replace(',', ' ').replace('&', ' ')
#     coord_str = coord_str.replace('o', '°').replace('’', "'").replace('”', '"')
#     coord_str = coord_str.upper()

#     try:
#         pattern = re.findall(r'(\d+)\s+(\d+)\s+(\d+)\s*([NSEW])', coord_str)
#         if len(pattern) >= 2:
#             lon = dms_to_dd(*pattern[0])
#             lat = dms_to_dd(*pattern[1])
#             return lat, lon
#     except:
#         pass

#     try:
#         pattern = re.findall(
#             r'([NS])\s*(\d+)[°O]?\s*(\d+)[\'′]\s*([\d.]+)["”]?\s*([EW])\s*(\d+)[°O]?\s*(\d+)[\'′]\s*([\d.]+)["”]?',
#             coord_str)
#         if pattern:
#             lat_d, lat_m, lat_s = pattern[0][1], pattern[0][2], pattern[0][3]
#             lon_d, lon_m, lon_s = pattern[0][5], pattern[0][6], pattern[0][7]
#             lat = dms_to_dd(lat_d, lat_m, lat_s, pattern[0][0])
#             lon = dms_to_dd(lon_d, lon_m, lon_s, pattern[0][4])
#             return lat, lon
#     except:
#         pass

#     return np.nan, np.nan

# # --- Load Excel ---
# file_path = "data/Active _Operational Mineral Tiles.xlsx"
# try:
#     df = pd.read_excel(file_path)
#     st.success("✅ Data loaded successfully.")
# except Exception as e:
#     st.error(f"❌ Failed to load file: {e}")
#     st.stop()

# # --- Parse Coordinates ---
# coord_col = "GEOGRAPHICAL COORDINATES OF THE MINERAL TITLE ( LONG. & LAT)"
# if coord_col not in df.columns:
#     st.error(f"Column '{coord_col}' not found.")
#     st.stop()

# df["Latitude"], df["Longitude"] = zip(*df[coord_col].apply(parse_coordinates))
# valid_coords = df.dropna(subset=["Latitude", "Longitude"]).copy()

# if valid_coords.empty:
#     st.warning("⚠️ No valid coordinates found.")
#     st.dataframe(df)
#     st.stop()

# # --- Google Maps Links ---
# valid_coords["📍 Coordinates"] = valid_coords.apply(
#     lambda row: f'<a href="https://www.google.com/maps?q={row["Latitude"]},{row["Longitude"]}" target="_blank">📍 View</a>',
#     axis=1
# )

# # --- Search ---
# search_text = st.text_input("🔍 Search by Title, State, or Activity:")
# if search_text:
#     filtered_df = valid_coords[valid_coords.apply(lambda row: search_text.lower() in str(row).lower(), axis=1)]
# else:
#     filtered_df = valid_coords

# # --- MAP FIRST ---
# st.markdown("### 🌍 Map View of Titles")
# m = folium.Map(
#     location=[filtered_df["Latitude"].mean(), filtered_df["Longitude"].mean()],
#     zoom_start=7, control_scale=True
# )
# marker_cluster = MarkerCluster().add_to(m)

# # --- Color by Activity ---
# color_palette = ['red', 'green', 'blue', 'purple', 'orange', 'darkred', 'gray']
# activity_col = "ACTIVITY" if "ACTIVITY" in filtered_df.columns else None
# categories = filtered_df[activity_col].unique().tolist() if activity_col else []
# color_map = {cat: color_palette[i % len(color_palette)] for i, cat in enumerate(categories)}

# for _, row in filtered_df.iterrows():
#     lat, lon = row["Latitude"], row["Longitude"]
#     title = row.get("TITLE", "No Title")
#     state = row.get("STATE", "")
#     activity = row.get(activity_col, "Other") if activity_col else "Other"
#     color = color_map.get(activity, "gray")

#     popup = f"<b>{title}</b><br>State: {state}<br>Activity: {activity}"
#     folium.Marker(
#         location=[lat, lon],
#         popup=popup,
#         tooltip=title,
#         icon=folium.Icon(color=color)
#     ).add_to(marker_cluster)

# st_folium(m, width=1200, height=700)

# # --- TABLE SECOND ---
# st.markdown("### 📋 Titles Table with Google Maps Links")
# st.write(filtered_df.to_html(escape=False, index=False), unsafe_allow_html=True)

# # --- DOWNLOAD BUTTONS ---
# st.markdown("### 📥 Download Filtered Data")

# # CSV
# csv_data = filtered_df.to_csv(index=False).encode("utf-8")
# st.download_button(
#     label="⬇️ Download CSV",
#     data=csv_data,
#     file_name="filtered_titles.csv",
#     mime="text/csv"
# )

# # Excel
# excel_buffer = io.BytesIO()
# with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
#     filtered_df.to_excel(writer, index=False, sheet_name="Titles")
# excel_data = excel_buffer.getvalue()
# st.download_button(
#     label="⬇️ Download Excel",
#     data=excel_data,
#     file_name="filtered_titles.xlsx",
#     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
# )

# #
# # import streamlit as st
# # import pandas as pd
# # import numpy as np
# # import folium
# # from folium.plugins import MarkerCluster
# # from streamlit_folium import st_folium
# # import re
# #
# # st.set_page_config(layout="wide")
# # st.title("🗺️ Map of Mineral Titles with Tooltips and Google Maps Links")
# #
# #
# # # --- Coordinate Parsing ---
# # def dms_to_dd(deg, minutes, seconds, direction):
# #     dd = float(deg) + float(minutes) / 60 + float(seconds) / 3600
# #     if direction.upper() in ['S', 'W']:
# #         dd *= -1
# #     return dd
# #
# #
# # def parse_coordinates(coord_str):
# #     if pd.isna(coord_str):
# #         return np.nan, np.nan
# #
# #     coord_str = coord_str.replace(',', ' ').replace('&', ' ')
# #     coord_str = coord_str.replace('o', '°').replace('’', "'").replace('”', '"')
# #     coord_str = coord_str.upper()
# #
# #     # Try DMS like "4 52 15E, 6 53 45N"
# #     try:
# #         pattern = re.findall(r'(\d+)\s+(\d+)\s+(\d+)\s*([NSEW])', coord_str)
# #         if len(pattern) >= 2:
# #             lon = dms_to_dd(*pattern[0])
# #             lat = dms_to_dd(*pattern[1])
# #             return lat, lon
# #     except:
# #         pass
# #
# #     # Try full fancy DMS like 'N 07° 24' 41.5" E 005° 14' 32.2"'
# #     try:
# #         pattern = re.findall(
# #             r'([NS])\s*(\d+)[°O]?\s*(\d+)[\'′]\s*([\d.]+)["”]?\s*([EW])\s*(\d+)[°O]?\s*(\d+)[\'′]\s*([\d.]+)["”]?',
# #             coord_str)
# #         if pattern:
# #             lat_d, lat_m, lat_s = pattern[0][1], pattern[0][2], pattern[0][3]
# #             lon_d, lon_m, lon_s = pattern[0][5], pattern[0][6], pattern[0][7]
# #             lat = dms_to_dd(lat_d, lat_m, lat_s, pattern[0][0])
# #             lon = dms_to_dd(lon_d, lon_m, lon_s, pattern[0][4])
# #             return lat, lon
# #     except:
# #         pass
# #
# #     return np.nan, np.nan
# #
# #
# # # --- Load Excel from Local Path (instead of file uploader) ---
# # local_excel_path = "data/Active _Operational Mineral Tiles.xlsx"  # 👉 Update this path as needed
# #
# # try:
# #     df = pd.read_excel(local_excel_path)
# #     st.success("✅ File loaded successfully from local path.")
# # except Exception as e:
# #     st.error(f"❌ Failed to load file. Error: {e}")
# #     st.stop()
# #
# # # --- Coordinate Processing ---
# # coord_col = "GEOGRAPHICAL COORDINATES OF THE MINERAL TITLE ( LONG. & LAT)"
# # if coord_col not in df.columns:
# #     st.error(f"Column '{coord_col}' not found in Excel file.")
# #     st.stop()
# #
# # df["Latitude"], df["Longitude"] = zip(*df[coord_col].apply(parse_coordinates))
# # valid_coords = df.dropna(subset=["Latitude", "Longitude"]).copy()
# #
# # if valid_coords.empty:
# #     st.warning("⚠️ No valid coordinates found.")
# #     st.dataframe(df)
# #     st.stop()
# #
# # # --- Add Google Maps Link ---
# # valid_coords["📍 Coordinates"] = valid_coords.apply(
# #     lambda row: f'<a href="https://www.google.com/maps?q={row["Latitude"]},{row["Longitude"]}" target="_blank">📍 View on Map</a>',
# #     axis=1
# # )
# #
# # # --- Search Filter ---
# # search_text = st.text_input("🔍 Search by Title, State, or anything:")
# # if search_text:
# #     filtered_df = valid_coords[valid_coords.apply(lambda row: search_text.lower() in str(row).lower(), axis=1)]
# # else:
# #     filtered_df = valid_coords
# #
# # # --- Show Table with Links ---
# # st.markdown("### 📄 Mineral Titles Table (with Google Maps Link)")
# # st.write(filtered_df.to_html(escape=False, index=False), unsafe_allow_html=True)
# #
# # # --- Map Visualization ---
# # st.markdown("### 🗺️ Map View")
# # m = folium.Map(location=[filtered_df["Latitude"].mean(), filtered_df["Longitude"].mean()], zoom_start=8,
# #                control_scale=True)
# # marker_cluster = MarkerCluster().add_to(m)
# #
# # # --- Color by Activity ---
# # color_palette = ['red', 'green', 'blue', 'purple', 'orange', 'darkred', 'lightgray']
# # category_column = "ACTIVITY" if "ACTIVITY" in filtered_df.columns else None
# # unique_categories = filtered_df[category_column].unique().tolist() if category_column else []
# # category_color_map = {cat: color_palette[i % len(color_palette)] for i, cat in enumerate(unique_categories)}
# #
# # for _, row in filtered_df.iterrows():
# #     lat, lon = row["Latitude"], row["Longitude"]
# #     title = row.get("TITLE", "No Title")
# #     state = row.get("STATE", "")
# #     activity = row.get(category_column, "Other") if category_column else "Other"
# #     color = category_color_map.get(activity, "gray")
# #
# #     popup_text = f"<b>{title}</b><br>State: {state}<br>Activity: {activity}"
# #     folium.Marker(
# #         location=[lat, lon],
# #         popup=popup_text,
# #         tooltip=title,
# #         icon=folium.Icon(color=color, icon="info-sign")
# #     ).add_to(marker_cluster)
# #
# # st_folium(m, width=1200, height=1000)
