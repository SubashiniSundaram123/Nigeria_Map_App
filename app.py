# import streamlit as st
# import pandas as pd
#
# st.title("📊 Excel Data Viewer")
#
# uploaded_file = st.file_uploader(r"C:\Users\dell\Downloads\Active _Operational Mineral Tiles.xlsx", type=["xlsx", "xls"])
#
# if uploaded_file:
#     df = pd.read_excel(uploaded_file)
#     st.success("File uploaded successfully!")
#     st.write("🔍 Preview of your data:")
#     st.dataframe(df)
#
#     # Example: Show basic stats
#     if st.checkbox("Show summary statistics"):
#         st.write(df.describe())

# import streamlit as st
# import pandas as pd
#
# st.set_page_config(page_title="Mining Titles Viewer", layout="wide")
# st.title("🪨 Nigerian Mining Titles Dashboard")
#
# uploaded_file = st.file_uploader(r"C:\Users\dell\Downloads\Active _Operational Mineral Tiles.xlsx", type=["xlsx"])
#
# if uploaded_file:
#     df = pd.read_excel(uploaded_file)
#
#     # Clean column names (remove whitespace)
#     df.columns = [col.strip() for col in df.columns]
#
#     st.success("✅ File uploaded successfully")
#
#     # Preview
#     st.subheader("📄 Data Preview")
#     st.dataframe(df)
#
#     # Filters
#     st.subheader("🔍 Filter Data")
#
#     col1, col2, col3 = st.columns(3)
#
#     with col1:
#         selected_state = st.multiselect("Filter by State", options=df["STATE"].dropna().unique())
#     with col2:
#         selected_activity = st.multiselect("Filter by Activity", options=df["Activity"].dropna().unique())
#     with col3:
#         selected_location = st.multiselect("Filter by Location Type", options=df["Location Type"].dropna().unique())
#
#     # Apply filters
#     if selected_state:
#         df = df[df["STATE"].isin(selected_state)]
#     if selected_activity:
#         df = df[df["Activity"].isin(selected_activity)]
#     if selected_location:
#         df = df[df["Location Type"].isin(selected_location)]
#
#     st.write(f"Filtered Rows: {len(df)}")
#
#     # Display with hyperlinks for InSAR images
#     st.subheader("🔗 View Titles with InSAR Image Links")
#
#     def make_clickable(link):
#         return f'<a href="{link}" target="_blank">View Image</a>' if pd.notna(link) else ''
#
#     df_display = df.copy()
#     if "InsarImages" in df.columns:
#         df_display["InsarImages"] = df_display["InsarImages"].apply(make_clickable)
#
#     st.write("📝 Filtered Data with Clickable Links")
#     st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
#
# else:
#     st.info("💡 Upload your Excel file to get started.")
#
# import streamlit as st
# import pandas as pd
# import numpy as np
# import pydeck as pdk
#
# st.set_page_config(page_title="Nigerian Mining Titles", layout="wide")
# st.title("🪨 Nigerian Mining Titles Dashboard")
#
# uploaded_file = st.file_uploader("📤 Upload your Excel file", type=["xlsx"])
#
# if uploaded_file:
#     df = pd.read_excel(uploaded_file)
#     df.columns = [col.strip() for col in df.columns]
#
#     # Initial preview
#     st.success("✅ File uploaded successfully")
#     st.subheader("📄 Data Preview")
#     st.dataframe(df)
#
#     # Filters
#     st.subheader("🔍 Filter Data")
#
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         selected_state = st.multiselect("Filter by State", df["STATE"].dropna().unique())
#     with col2:
#         selected_activity = st.multiselect("Filter by Activity", df["Activity"].dropna().unique())
#     with col3:
#         selected_location = st.multiselect("Filter by Location Type", df["Location Type"].dropna().unique())
#
#     # Apply filters
#     filtered_df = df.copy()
#     if selected_state:
#         filtered_df = filtered_df[filtered_df["STATE"].isin(selected_state)]
#     if selected_activity:
#         filtered_df = filtered_df[filtered_df["Activity"].isin(selected_activity)]
#     if selected_location:
#         filtered_df = filtered_df[filtered_df["Location Type"].isin(selected_location)]
#
#     st.write(f"🎯 Filtered Rows: {len(filtered_df)}")
#
#     # Add clickable links
#     st.subheader("🔗 View Titles with InSAR Image Links")
#
#     def make_clickable(link):
#         return f'<a href="{link}" target="_blank">View Image</a>' if pd.notna(link) else ''
#
#     df_display = filtered_df.copy()
#     if "InsarImages" in df_display.columns:
#         df_display["InsarImages"] = df_display["InsarImages"].apply(make_clickable)
#
#     st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
#
#     # Map coordinates section
#     st.subheader("🗺️ Map of Mineral Titles with Tooltips")
#
#     coord_col = "GEOGRAPHICAL COORDINATES OF THE MINERAL TITLE ( LONG. & LAT)"
#
#     def extract_lat_lon(coord_str):
#         try:
#             if pd.isna(coord_str): return np.nan, np.nan
#             parts = coord_str.split(",")
#             if len(parts) != 2: return np.nan, np.nan
#             lon, lat = map(str.strip, parts)
#             return float(lat), float(lon)
#         except:
#             return np.nan, np.nan
#
#     if coord_col in filtered_df.columns:
#         filtered_df["Latitude"], filtered_df["Longitude"] = zip(*filtered_df[coord_col].apply(extract_lat_lon))
#         map_df = filtered_df.dropna(subset=["Latitude", "Longitude"])
#
#         if not map_df.empty:
#             st.pydeck_chart(pdk.Deck(
#                 map_style='mapbox://styles/mapbox/light-v9',
#                 initial_view_state=pdk.ViewState(
#                     latitude=map_df["Latitude"].mean(),
#                     longitude=map_df["Longitude"].mean(),
#                     zoom=5,
#                     pitch=30,
#                 ),
#                 layers=[
#                     pdk.Layer(
#                         'ScatterplotLayer',
#                         data=map_df,
#                         get_position='[Longitude, Latitude]',
#                         get_color='[200, 30, 0, 160]',
#                         get_radius=10000,
#                         pickable=True,
#                     )
#                 ],
#                 tooltip={"text": "Title No: {Title Number}\nState: {STATE}\nActivity: {Activity}"}
#             ))
#         else:
#             st.warning("⚠️ No valid coordinates found for selected filters.")
#     else:
#         st.warning(f"⚠️ Column '{coord_col}' not found in the uploaded file.")
# else:
#     st.info("💡 Please upload your Excel file to begin.")
#
# import streamlit as st
# import pandas as pd
# import numpy as np
# import pydeck as pdk
#
# st.set_page_config(page_title="Nigerian Mining Titles", layout="wide")
# st.title("🪨 Nigerian Mining Titles Dashboard")
#
# uploaded_file = st.file_uploader("📤 Upload your Excel file", type=["xlsx"])
#
# # --- Conversion helpers ---
#
# def dms_to_dd(dms_str):
#     try:
#         parts = dms_str.strip().replace("°", "").replace("′", "").replace("″", "").split()
#         if len(parts) != 3:
#             return np.nan
#         deg, minutes, seconds = map(float, parts[:3])
#         return deg + (minutes / 60) + (seconds / 3600)
#     except:
#         return np.nan
#
# def extract_lat_lon_dms(dms_coord):
#     try:
#         if pd.isna(dms_coord): return np.nan, np.nan
#         dms_coord = dms_coord.replace(",", "")
#         parts = dms_coord.split()
#         if len(parts) < 6: return np.nan, np.nan
#
#         lon_dms = f"{parts[0]} {parts[1]} {parts[2]}"
#         lat_dms = f"{parts[3]} {parts[4]} {parts[5]}"
#
#         lon = dms_to_dd(lon_dms)
#         lat = dms_to_dd(lat_dms)
#
#         if "W" in dms_coord.upper(): lon *= -1
#         if "S" in dms_coord.upper(): lat *= -1
#
#         return lat, lon
#     except:
#         return np.nan, np.nan
#
# def make_clickable(link):
#     return f'<a href="{link}" target="_blank">View Image</a>' if pd.notna(link) else ''
#
# # --- Main app ---
#
# if uploaded_file:
#     df = pd.read_excel(uploaded_file)
#     df.columns = [col.strip() for col in df.columns]
#
#     st.success("✅ File uploaded successfully")
#
#     st.subheader("📄 Data Preview")
#     st.dataframe(df)
#
#     st.subheader("🔍 Filter Data")
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         selected_state = st.multiselect("Filter by State", df["STATE"].dropna().unique())
#     with col2:
#         selected_activity = st.multiselect("Filter by Activity", df["Activity"].dropna().unique())
#     with col3:
#         selected_location = st.multiselect("Filter by Location Type", df["Location Type"].dropna().unique())
#
#     filtered_df = df.copy()
#     if selected_state:
#         filtered_df = filtered_df[filtered_df["STATE"].isin(selected_state)]
#     if selected_activity:
#         filtered_df = filtered_df[filtered_df["Activity"].isin(selected_activity)]
#     if selected_location:
#         filtered_df = filtered_df[filtered_df["Location Type"].isin(selected_location)]
#
#     st.write(f"🎯 Filtered Rows: {len(filtered_df)}")
#
#     st.subheader("🔗 View Titles with InSAR Image Links")
#     df_display = filtered_df.copy()
#     if "InsarImages" in df_display.columns:
#         df_display["InsarImages"] = df_display["InsarImages"].apply(make_clickable)
#     st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
#
#     st.subheader("🗺️ Map of Mineral Titles with Tooltips")
#
#     coord_col = "GEOGRAPHICAL COORDINATES OF THE MINERAL TITLE ( LAT  & LONG.)"
#     if coord_col in filtered_df.columns:
#         filtered_df["Latitude"], filtered_df["Longitude"] = zip(*filtered_df[coord_col].apply(extract_lat_lon_dms))
#         map_df = filtered_df.dropna(subset=["Latitude", "Longitude"])
#
#         if not map_df.empty:
#             st.pydeck_chart(pdk.Deck(
#                 map_style='mapbox://styles/mapbox/light-v9',
#                 initial_view_state=pdk.ViewState(
#                     latitude=map_df["Latitude"].mean(),
#                     longitude=map_df["Longitude"].mean(),
#                     zoom=5,
#                     pitch=30,
#                 ),
#                 layers=[
#                     pdk.Layer(
#                         'ScatterplotLayer',
#                         data=map_df,
#                         get_position='[Longitude, Latitude]',
#                         get_color='[0, 100, 200, 160]',
#                         get_radius=10000,
#                         pickable=True,
#                     )
#                 ],
#                 tooltip={"text": "📍 Title: {Title Number}\n📌 State: {STATE}\n🔧 Activity: {Activity}"}
#             ))
#         else:
#             st.warning("⚠️ No valid coordinates found for selected filters.")
#     else:
#         st.warning(f"⚠️ Column '{coord_col}' not found in the uploaded file.")
# else:
#     st.info("💡 Please upload your Excel file to begin.")
# #
# import streamlit as st
# import pandas as pd
# import numpy as np
# import pydeck as pdk
# from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
#
# st.set_page_config(page_title="Nigerian Mining Titles", layout="wide")
# st.title("🪨 Nigerian Mining Titles Dashboard")
#
# uploaded_file = st.file_uploader("📤 Upload your Excel file", type=["xlsx"])
#
# # --- Coordinate Conversion ---
#
# def dms_to_dd(dms_str):
#     try:
#         parts = dms_str.strip().split()
#         deg, minutes, seconds = map(float, parts[:3])
#         return deg + (minutes / 60) + (seconds / 3600)
#     except:
#         return np.nan
#
# def extract_lat_lon_dms(dms_coord):
#     try:
#         if pd.isna(dms_coord): return np.nan, np.nan
#         dms_coord = dms_coord.replace(",", "").replace("E", " E").replace("W", " W").replace("N", " N").replace("S", " S")
#         parts = dms_coord.split()
#         if len(parts) < 6:
#             return np.nan, np.nan
#         lon_dms = f"{parts[0]} {parts[1]} {parts[2]}"
#         lat_dms = f"{parts[3]} {parts[4]} {parts[5]}"
#         lon = dms_to_dd(lon_dms)
#         lat = dms_to_dd(lat_dms)
#         if "W" in parts[2].upper(): lon *= -1
#         if "S" in parts[5].upper(): lat *= -1
#         return lat, lon
#     except:
#         return np.nan, np.nan
#
# # --- Main App Logic ---
#
# if uploaded_file:
#     df = pd.read_excel(uploaded_file)
#     df.columns = [col.strip() for col in df.columns]
#
#     coord_col = "GEOGRAPHICAL COORDINATES OF THE MINERAL TITLE ( LONG. & LAT)"
#     df["Latitude"], df["Longitude"] = zip(*df[coord_col].apply(extract_lat_lon_dms))
#     map_df = df.dropna(subset=["Latitude", "Longitude"])
#
#     st.subheader("📄 Interactive Data Table (Click to Highlight on Map)")
#     gb = GridOptionsBuilder.from_dataframe(map_df)
#     gb.configure_selection('single', use_checkbox=True)
#     gb.configure_column(coord_col, header_name="📍 Geo Coordinates", cellStyle={'color': 'blue', 'textDecoration': 'underline'})
#     grid_options = gb.build()
#
#     grid_response = AgGrid(map_df, gridOptions=grid_options, update_mode=GridUpdateMode.SELECTION_CHANGED,
#                            height=300, fit_columns_on_grid_load=True)
#
#     selected = grid_response['selected_rows']
#     if selected:
#         lat = selected[0]['Latitude']
#         lon = selected[0]['Longitude']
#         selected_point = [[lon, lat]]
#         zoom = 10
#     else:
#         selected_point = None
#         lat = map_df["Latitude"].mean()
#         lon = map_df["Longitude"].mean()
#         zoom = 5
#
#     st.subheader("🗺️ Interactive Map of Titles")
#     layers = [
#         pdk.Layer(
#             "ScatterplotLayer",
#             data=map_df,
#             get_position='[Longitude, Latitude]',
#             get_color='[0, 100, 200, 160]',
#             get_radius=10000,
#             pickable=True,
#         )
#     ]
#
#     if selected_point:
#         layers.append(
#             pdk.Layer(
#                 "ScatterplotLayer",
#                 data=pd.DataFrame([{"Longitude": lon, "Latitude": lat}]),
#                 get_position='[Longitude, Latitude]',
#                 get_color='[255, 0, 0, 200]',
#                 get_radius=15000,
#             )
#         )
#
#     st.pydeck_chart(pdk.Deck(
#         map_style='mapbox://styles/mapbox/light-v9',
#         initial_view_state=pdk.ViewState(
#             latitude=lat,
#             longitude=lon,
#             zoom=zoom,
#             pitch=30,
#         ),
#         layers=layers,
#         tooltip={"text": "📍 {Title Number} \n📌 {STATE} \n🔧 {Activity}"}
#     ))
# else:
#     st.info("💡 Upload an Excel file to begin.")
#
# import streamlit as st
# import pandas as pd
# import numpy as np
# import pydeck as pdk
#
# st.set_page_config(page_title="Nigerian Mining Titles", layout="wide")
# st.title("🪨 Nigerian Mining Titles Dashboard")
#
# uploaded_file = st.file_uploader("📤 Upload your Excel file", type=["xlsx"])
#
# # --- Conversion helpers ---
#
# def dms_to_dd(dms_str):
#     try:
#         parts = dms_str.strip().replace("°", "").replace("′", "").replace("″", "").split()
#         if len(parts) != 3:
#             return np.nan
#         deg, minutes, seconds = map(float, parts[:3])
#         return deg + (minutes / 60) + (seconds / 3600)
#     except:
#         return np.nan
#
# def extract_lat_lon_dms(dms_coord):
#     try:
#         if pd.isna(dms_coord): return np.nan, np.nan
#         dms_coord = dms_coord.replace(",", "")
#         parts = dms_coord.split()
#         if len(parts) < 6: return np.nan, np.nan
#
#         lon_dms = f"{parts[0]} {parts[1]} {parts[2]}"
#         lat_dms = f"{parts[3]} {parts[4]} {parts[5]}"
#
#         lon = dms_to_dd(lon_dms)
#         lat = dms_to_dd(lat_dms)
#
#         if "W" in dms_coord.upper(): lon *= -1
#         if "S" in dms_coord.upper(): lat *= -1
#
#         return lat, lon
#     except:
#         return np.nan, np.nan
#
# def make_clickable(link):
#     return f'<a href="{link}" target="_blank">View Image</a>' if pd.notna(link) else ''
#
# # --- Main app ---
#
# if uploaded_file:
#     df = pd.read_excel(uploaded_file)
#     df.columns = [col.strip() for col in df.columns]
#
#     st.success("✅ File uploaded successfully")
#
#     st.subheader("📄 Data Preview")
#     st.dataframe(df)
#
#     st.subheader("🔍 Filter Data")
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         selected_state = st.multiselect("Filter by State", df["STATE"].dropna().unique())
#     with col2:
#         selected_activity = st.multiselect("Filter by Activity", df["Activity"].dropna().unique())
#     with col3:
#         selected_location = st.multiselect("Filter by Location Type", df["Location Type"].dropna().unique())
#
#     filtered_df = df.copy()
#     if selected_state:
#         filtered_df = filtered_df[filtered_df["STATE"].isin(selected_state)]
#     if selected_activity:
#         filtered_df = filtered_df[filtered_df["Activity"].isin(selected_activity)]
#     if selected_location:
#         filtered_df = filtered_df[filtered_df["Location Type"].isin(selected_location)]
#
#     st.write(f"🎯 Filtered Rows: {len(filtered_df)}")
#
#     st.subheader("🔗 View Titles with InSAR Image Links")
#     df_display = filtered_df.copy()
#     if "InsarImages" in df_display.columns:
#         df_display["InsarImages"] = df_display["InsarImages"].apply(make_clickable)
#     st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
#
#     st.subheader("🗺️ Map of Mineral Titles with Tooltips")
#
#     coord_col = "GEOGRAPHICAL COORDINATES OF THE MINERAL TITLE ( LONG. & LAT)"
#     if coord_col in filtered_df.columns:
#         filtered_df["Latitude"], filtered_df["Longitude"] = zip(*filtered_df[coord_col].apply(extract_lat_lon_dms))
#         map_df = filtered_df.dropna(subset=["Latitude", "Longitude"])
#
#         if not map_df.empty:
#             st.pydeck_chart(pdk.Deck(
#                 map_style='mapbox://styles/mapbox/light-v9',
#                 initial_view_state=pdk.ViewState(
#                     latitude=map_df["Latitude"].mean(),
#                     longitude=map_df["Longitude"].mean(),
#                     zoom=5,
#                     pitch=30,
#                 ),
#                 layers=[
#                     pdk.Layer(
#                         'ScatterplotLayer',
#                         data=map_df,
#                         get_position='[Longitude, Latitude]',
#                         get_color='[0, 100, 200, 160]',
#                         get_radius=10000,
#                         pickable=True,
#                     )
#                 ],
#                 tooltip={"text": "📍 Title: {Title Number}\n📌 State: {STATE}\n🔧 Activity: {Activity}"}
#             ))
#         else:
#             st.warning("⚠️ No valid coordinates found for selected filters.")
#     else:
#         st.warning(f"⚠️ Column '{coord_col}' not found in the uploaded file.")
# else:
#     st.info("💡 Please upload your Excel file to begin.")

# import streamlit as st
# import pandas as pd
# import numpy as np
# import folium
# from folium.plugins import MarkerCluster
# from streamlit_folium import st_folium
# import re
#
# st.set_page_config(layout="wide")
#
# st.title("🗺️ Map of Mineral Titles with Tooltips")
# uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
#
#
# # --- Coordinate Parsing ---
# def dms_to_dd(deg, minutes, seconds, direction):
#     dd = float(deg) + float(minutes) / 60 + float(seconds) / 3600
#     if direction.upper() in ['S', 'W']:
#         dd *= -1
#     return dd
#
#
# def parse_coordinates(coord_str):
#     if pd.isna(coord_str):
#         return np.nan, np.nan
#
#     coord_str = coord_str.replace(',', ' ').replace('&', ' ')
#     coord_str = coord_str.replace('o', '°').replace('’', "'").replace('”', '"')
#     coord_str = coord_str.upper()
#
#     # Try DMS like "4 52 15E, 6 53 45N"
#     try:
#         pattern = re.findall(r'(\d+)\s+(\d+)\s+(\d+)\s*([NSEW])', coord_str)
#         if len(pattern) >= 2:
#             lon = dms_to_dd(*pattern[0])
#             lat = dms_to_dd(*pattern[1])
#             return lat, lon
#     except:
#         pass
#
#     # Try full fancy DMS like 'N 07° 24' 41.5" E 005° 14' 32.2"'
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
#
#     return np.nan, np.nan
#
#
# # --- App Logic ---
# if uploaded_file:
#     df = pd.read_excel(uploaded_file)
#     coord_col = "GEOGRAPHICAL COORDINATES OF THE MINERAL TITLE ( LONG. & LAT)"
#
#     if coord_col not in df.columns:
#         st.error(f"Column '{coord_col}' not found in Excel file.")
#         st.stop()
#
#     df["Latitude"], df["Longitude"] = zip(*df[coord_col].apply(parse_coordinates))
#     valid_coords = df.dropna(subset=["Latitude", "Longitude"])
#
#     if valid_coords.empty:
#         st.warning("⚠️ No valid coordinates found for selected filters.")
#         st.dataframe(df)
#         st.stop()
#
#     # --- Search Box ---
#     search_text = st.text_input("🔍 Search by Title or State:")
#     if search_text:
#         filtered_df = valid_coords[valid_coords.apply(lambda row: search_text.lower() in str(row).lower(), axis=1)]
#     else:
#         filtered_df = valid_coords
#
#     # --- Display Table ---
#     st.subheader("📄 Mineral Titles Table (Click a row to zoom to point on map)")
#     selected_row = st.data_editor(
#         filtered_df,
#         column_order=None,
#         hide_index=True,
#         use_container_width=True,
#         num_rows="dynamic",
#         key="data_editor"
#     )
#
#     # --- Map ---
#     m = folium.Map(location=[filtered_df["Latitude"].mean(), filtered_df["Longitude"].mean()], zoom_start=7)
#     marker_cluster = MarkerCluster().add_to(m)
#
#     for _, row in filtered_df.iterrows():
#         title = row.get("TITLE", "")
#         state = row.get("STATE", "")
#         tooltip = f"{title} ({state})" if state else title
#         folium.Marker(
#             location=[row["Latitude"], row["Longitude"]],
#             popup=tooltip,
#             tooltip=tooltip,
#             icon=folium.Icon(color="blue", icon="map-pin", prefix="fa")
#         ).add_to(marker_cluster)
#
#     # --- Zoom on Selection ---
#     if not selected_row.empty:
#         lat = selected_row["Latitude"].values[0]
#         lon = selected_row["Longitude"].values[0]
#         m.location = [lat, lon]
#         m.zoom_start = 14
#
#     st_data = st_folium(m, width=1000, height=500)
#
# import streamlit as st
# import pandas as pd
# import folium
# from folium.plugins import MarkerCluster
# from streamlit_folium import st_folium
#
# st.set_page_config(layout="wide")
# st.title("🗺️ Map of Mineral Titles with Interactive Selection")
#
# uploaded_file = st.file_uploader("📄 Upload your Excel file", type=["xlsx"])
#
# if uploaded_file:
#     df = pd.read_excel(uploaded_file)
#
#     # 🧪 Identify correct column names
#     lat_col = "Latitude"
#     lon_col = "Longitude"
#
#     if lat_col not in df.columns or lon_col not in df.columns:
#         st.error("Latitude and Longitude columns not found. Please check your Excel headers.")
#         st.stop()
#
#     # Remove invalid coords
#     df = df.dropna(subset=[lat_col, lon_col])
#     df = df[df[lat_col].apply(lambda x: isinstance(x, (int, float)))]
#     df = df[df[lon_col].apply(lambda x: isinstance(x, (int, float)))]
#
#     # 🔍 Optional search
#     search = st.text_input("Search by title, state or other details")
#     if search:
#         filtered_df = df[df.apply(lambda row: search.lower() in str(row).lower(), axis=1)]
#     else:
#         filtered_df = df
#
#     st.subheader("📋 Click on a row to zoom in on the map")
#     clicked = st.data_editor(
#         filtered_df,
#         hide_index=True,
#         use_container_width=True,
#         num_rows="dynamic",
#         key="table"
#     )
#
#     # Default map view
#     map_lat = filtered_df[lat_col].mean()
#     map_lon = filtered_df[lon_col].mean()
#     zoom = 7
#
#     # If user clicked a row
#     if not clicked.empty:
#         map_lat = clicked.iloc[0][lat_col]
#         map_lon = clicked.iloc[0][lon_col]
#         zoom = 14
#
#     # 🗺️ Create map
#     m = folium.Map(location=[map_lat, map_lon], zoom_start=zoom)
#     marker_cluster = MarkerCluster().add_to(m)
#
#     for _, row in filtered_df.iterrows():
#         tooltip = row.get("TITLE", "No Title")
#         folium.Marker(
#             location=[row[lat_col], row[lon_col]],
#             tooltip=tooltip,
#             popup=tooltip,
#             icon=folium.Icon(color='blue', icon='map-marker', prefix='fa')
#         ).add_to(marker_cluster)
#
#     st_folium(m, width=1000, height=500)
#
# import streamlit as st
# import pandas as pd
# import numpy as np
# import folium
# from folium.plugins import MarkerCluster
# from streamlit_folium import st_folium
# import re
#
# st.set_page_config(layout="wide")
# st.title("🗺️ Map of Mineral Titles with Tooltips")
#
# uploaded_file = st.file_uploader("📄 Upload your Excel file", type=["xlsx"])
#
# # --- Coordinate Parsing ---
# def dms_to_dd(deg, minutes, seconds, direction):
#     dd = float(deg) + float(minutes)/60 + float(seconds)/3600
#     if direction.upper() in ['S', 'W']:
#         dd *= -1
#     return dd
#
# def parse_coordinates(coord_str):
#     if pd.isna(coord_str):
#         return np.nan, np.nan
#
#     coord_str = coord_str.replace(',', ' ').replace('&', ' ')
#     coord_str = coord_str.replace('o', '°').replace('’', "'").replace('”', '"')
#     coord_str = coord_str.upper()
#
#     try:
#         # Pattern 1: 4 52 15E, 6 53 45N
#         pattern = re.findall(r'(\d+)\s+(\d+)\s+([\d.]+)\s*([NSEW])', coord_str)
#         if len(pattern) >= 2:
#             lon = dms_to_dd(*pattern[0])
#             lat = dms_to_dd(*pattern[1])
#             return lat, lon
#     except:
#         pass
#
#     try:
#         # Pattern 2: N 07° 24' 41.5" E 005° 14' 32.2"
#         pattern = re.findall(r'([NS])\s*(\d+)[°O]?\s*(\d+)[\'′]\s*([\d.]+)["”]?\s*([EW])\s*(\d+)[°O]?\s*(\d+)[\'′]\s*([\d.]+)["”]?', coord_str)
#         if pattern:
#             lat_d, lat_m, lat_s = pattern[0][1], pattern[0][2], pattern[0][3]
#             lon_d, lon_m, lon_s = pattern[0][5], pattern[0][6], pattern[0][7]
#             lat = dms_to_dd(lat_d, lat_m, lat_s, pattern[0][0])
#             lon = dms_to_dd(lon_d, lon_m, lon_s, pattern[0][4])
#             return lat, lon
#     except:
#         pass
#
#     return np.nan, np.nan
#
# # --- App Logic ---
# if uploaded_file:
#     df = pd.read_excel(uploaded_file)
#     coord_col = "GEOGRAPHICAL COORDINATES OF THE MINERAL TITLE ( LONG. & LAT)"
#
#     if coord_col not in df.columns:
#         st.error(f"❌ Column '{coord_col}' not found in Excel file.")
#         st.stop()
#
#     df["Latitude"], df["Longitude"] = zip(*df[coord_col].apply(parse_coordinates))
#     valid_coords = df.dropna(subset=["Latitude", "Longitude"])
#
#     if valid_coords.empty:
#         st.warning("⚠️ No valid coordinates found.")
#         st.dataframe(df)
#         st.stop()
#
#     # --- Search ---
#     search_text = st.text_input("🔍 Search by Title or State:")
#     if search_text:
#         filtered_df = valid_coords[valid_coords.apply(lambda row: search_text.lower() in str(row).lower(), axis=1)]
#     else:
#         filtered_df = valid_coords
#
#     # --- Display Table ---
#     st.subheader("📋 Click a row to zoom to the location")
#     selected_rows = st.data_editor(
#         filtered_df,
#         column_order=None,
#         hide_index=True,
#         use_container_width=True,
#         num_rows="dynamic",
#         key="row_selection"
#     )
#
#     # --- Map Creation ---
#     default_lat = filtered_df["Latitude"].mean()
#     default_lon = filtered_df["Longitude"].mean()
#     zoom_level = 14
#
#     # Zoom in if user selects a row
#     if not selected_rows.empty:
#         default_lat = selected_rows["Latitude"].values[0]
#         default_lon = selected_rows["Longitude"].values[0]
#         zoom_level = 18
#
#     m = folium.Map(location=[default_lat, default_lon], zoom_start=zoom_level)
#     marker_cluster = MarkerCluster().add_to(m)
#
#     for _, row in filtered_df.iterrows():
#         tooltip = f"{row.get('TITLE', 'No Title')} ({row.get('STATE', '')})"
#         folium.Marker(
#             location=[row["Latitude"], row["Longitude"]],
#             popup=tooltip,
#             tooltip=tooltip,
#             icon=folium.Icon(color="blue", icon="map-pin", prefix="fa")
#         ).add_to(marker_cluster)
#
#     # Show the final interactive map
#     st_folium(m, width=None, height=1600)  # Full width and taller height
#

# import streamlit as st
# import pandas as pd
# import numpy as np
# import folium
# from folium.plugins import MarkerCluster
# from streamlit_folium import st_folium
# import re
# from itertools import cycle
#
# st.set_page_config(layout="wide")
#
# st.title("🗺️ Map of Mineral Titles with Tooltips & Category Colors")
# uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
#
#
# # --- Coordinate Parsing ---
# def dms_to_dd(deg, minutes, seconds, direction):
#     dd = float(deg) + float(minutes) / 60 + float(seconds) / 3600
#     if direction.upper() in ['S', 'W']:
#         dd *= -1
#     return dd
#
#
# def parse_coordinates(coord_str):
#     if pd.isna(coord_str):
#         return np.nan, np.nan
#
#     coord_str = coord_str.replace(',', ' ').replace('&', ' ')
#     coord_str = coord_str.replace('o', '°').replace('’', "'").replace('”', '"')
#     coord_str = coord_str.upper()
#
#     try:
#         pattern = re.findall(r'(\d+)\s+(\d+)\s+(\d+)\s*([NSEW])', coord_str)
#         if len(pattern) >= 2:
#             lon = dms_to_dd(*pattern[0])
#             lat = dms_to_dd(*pattern[1])
#             return lat, lon
#     except:
#         pass
#
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
#
#     return np.nan, np.nan
#
#
# if uploaded_file:
#     df = pd.read_excel(uploaded_file)
#     coord_col = "GEOGRAPHICAL COORDINATES OF THE MINERAL TITLE ( LONG. & LAT)"
#
#     if coord_col not in df.columns:
#         st.error(f"Column '{coord_col}' not found in Excel file.")
#         st.stop()
#
#     df["Latitude"], df["Longitude"] = zip(*df[coord_col].apply(parse_coordinates))
#     valid_coords = df.dropna(subset=["Latitude", "Longitude"])
#
#     if valid_coords.empty:
#         st.warning("⚠️ No valid coordinates found for selected filters.")
#         st.dataframe(df)
#         st.stop()
#
#     # --- Search ---
#     search_text = st.text_input("🔍 Search by Title or State:")
#     if search_text:
#         filtered_df = valid_coords[valid_coords.apply(lambda row: search_text.lower() in str(row).lower(), axis=1)]
#     else:
#         filtered_df = valid_coords
#
#     # --- Category Coloring ---
#     category_options = ["Mine Area", "Location Type", "Activity", "Vehicles"]
#     available_columns = [col for col in df.columns]
#
#     # Normalize both sides to match real columns
#     category_mapping = {}
#     for opt in category_options:
#         normalized_key = opt.upper().replace(" ", "_")
#         for col in available_columns:
#             if col.upper().replace(" ", "_") == normalized_key:
#                 category_mapping[opt] = col
#                 break
#
#     if category_mapping:
#         selected_category = st.selectbox("🎨 Color markers by:", list(category_mapping.keys()))
#         category_column_key = category_mapping[selected_category]
#     else:
#         st.warning("⚠️ No matching category columns found in your Excel file.")
#         category_column_key = None
#
#     # category_options = ["Mine Area", "Location Type", "Activity", "Vehicles"]
#     # existing_options = [opt for opt in category_options if opt.upper().replace(" ", "_") in df.columns]
#     # category_column = st.selectbox("🎨 Color markers by:", existing_options)
#     #
#     # category_column_key = category_column.upper().replace(" ", "_")
#
#     color_palette = cycle([
#         "blue", "green", "red", "purple", "orange",
#         "darkred", "lightgray", "cadetblue", "darkblue", "black"
#     ])
#     if category_column_key:
#         category_values = filtered_df[category_column_key].dropna().unique()
#         color_map = {val: next(color_palette) for val in category_values}
#     else:
#         color_map = {}
#
#     # category_values = filtered_df[category_column_key].dropna().unique()
#     # color_map = {val: next(color_palette) for val in category_values}
#
#     # --- Display Table with Filters ---
#     st.subheader("📄 Mineral Titles Table (Click a row to zoom to point on map)")
#     selected_row = st.data_editor(
#         filtered_df,
#         column_order=None,
#         hide_index=True,
#         use_container_width=True,
#         num_rows="dynamic",
#         key="data_editor",
#         column_config={
#             "TITLE": st.column_config.TextColumn("Title"),
#             "STATE": st.column_config.TextColumn("State"),
#             "Latitude": st.column_config.NumberColumn("Latitude"),
#             "Longitude": st.column_config.NumberColumn("Longitude"),
#         }
#     )
#
#     # --- Map Display ---
#     m = folium.Map(location=[filtered_df["Latitude"].mean(), filtered_df["Longitude"].mean()], zoom_start=6)
#     marker_cluster = MarkerCluster().add_to(m)
#
#     for _, row in filtered_df.iterrows():
#         title = row.get("TITLE", "")
#         state = row.get("STATE", "")
#         category_value = row.get(category_column_key, "Unknown")
#         marker_color = color_map.get(category_value, "gray")
#
#         tooltip = f"{title} ({state})"
#         popup_text = f"<b>{title}</b><br>State: {state}<br>{category_column}: {category_value}"
#
#         folium.Marker(
#             location=[row["Latitude"], row["Longitude"]],
#             popup=popup_text,
#             tooltip=tooltip,
#             icon=folium.Icon(color=marker_color, icon="map-pin", prefix="fa")
#         ).add_to(marker_cluster)
#
#     # --- Zoom on Selection ---
#     if not selected_row.empty:
#         lat = selected_row["Latitude"].values[0]
#         lon = selected_row["Longitude"].values[0]
#         m.location = [lat, lon]
#         m.zoom_start = 14
#
#     # Big Map Display
#     st_data = st_folium(m, width=1200, height=700)
#
#     # --- Legend ---
#     with st.expander("🧾 Marker Color Legend"):
#         for val, color in color_map.items():
#             st.markdown(f"<span style='color:{color}'>⬤</span> {val}", unsafe_allow_html=True)

# import streamlit as st
# import pandas as pd
# import numpy as np
# import folium
# from folium.plugins import MarkerCluster
# from streamlit_folium import st_folium
# import re
# import itertools
#
# st.set_page_config(layout="wide")
#
# st.title("🗺️ Map of Mineral Titles with Tooltips")
# uploaded_file = st.file_uploader("📤 Upload your Excel file", type=["xlsx"])
#
# # --- Coordinate Parsing ---
# def dms_to_dd(deg, minutes, seconds, direction):
#     dd = float(deg) + float(minutes)/60 + float(seconds)/3600
#     if direction.upper() in ['S', 'W']:
#         dd *= -1
#     return dd
#
# def parse_coordinates(coord_str):
#     if pd.isna(coord_str):
#         return np.nan, np.nan
#
#     coord_str = coord_str.replace(',', ' ').replace('&', ' ')
#     coord_str = coord_str.replace('o', '°').replace('’', "'").replace('”', '"')
#     coord_str = coord_str.upper()
#
#     # Try DMS like "4 52 15E, 6 53 45N"
#     try:
#         pattern = re.findall(r'(\d+)\s+(\d+)\s+([\d.]+)\s*([NSEW])', coord_str)
#         if len(pattern) >= 2:
#             lon = dms_to_dd(*pattern[0])
#             lat = dms_to_dd(*pattern[1])
#             return lat, lon
#     except:
#         pass
#
#     # Try full fancy DMS like 'N 07° 24' 41.5" E 005° 14' 32.2"'
#     try:
#         pattern = re.findall(r'([NS])\s*(\d+)[°O]?\s*(\d+)[\'′]\s*([\d.]+)["”]?\s*[&]?\s*([EW])\s*(\d+)[°O]?\s*(\d+)[\'′]\s*([\d.]+)["”]?', coord_str)
#         if pattern:
#             lat = dms_to_dd(pattern[0][1], pattern[0][2], pattern[0][3], pattern[0][0])
#             lon = dms_to_dd(pattern[0][5], pattern[0][6], pattern[0][7], pattern[0][4])
#             return lat, lon
#     except:
#         pass
#
#     return np.nan, np.nan
#
# # --- App Logic ---
# if uploaded_file:
#     df = pd.read_excel(uploaded_file)
#
#     coord_col = "GEOGRAPHICAL COORDINATES OF THE MINERAL TITLE ( LONG. & LAT)"
#     if coord_col not in df.columns:
#         st.error(f"Column '{coord_col}' not found in Excel file.")
#         st.stop()
#
#     df["Latitude"], df["Longitude"] = zip(*df[coord_col].apply(parse_coordinates))
#     valid_coords = df.dropna(subset=["Latitude", "Longitude"])
#
#     if valid_coords.empty:
#         st.warning("⚠️ No valid coordinates found for selected filters.")
#         st.dataframe(df)
#         st.stop()
#
#     # --- Optional Color-Coding by Category ---
#     category_options = ["Mine Area", "Location Type", "Activity", "Vehicles"]
#     available_columns = list(df.columns)
#
#     # Map available category options to actual columns
#     category_mapping = {}
#     for opt in category_options:
#         norm_opt = opt.upper().replace(" ", "_")
#         for col in available_columns:
#             if col.upper().replace(" ", "_") == norm_opt:
#                 category_mapping[opt] = col
#                 break
#
#     selected_category = None
#     category_column_key = None
#
#     if category_mapping:
#         selected_category = st.selectbox("🎨 Color markers by:", list(category_mapping.keys()))
#         category_column_key = category_mapping[selected_category]
#
#     # --- Filter Table ---
#     st.subheader("📄 Mineral Titles Table (Click a row to zoom to map location)")
#     search_text = st.text_input("🔍 Search by Title, State, or other details:")
#     filtered_df = valid_coords
#
#     if search_text:
#         filtered_df = valid_coords[valid_coords.apply(lambda row: search_text.lower() in str(row).lower(), axis=1)]
#
#     selected_row = st.data_editor(
#         filtered_df,
#         column_order=None,
#         hide_index=True,
#         use_container_width=True,
#         num_rows="dynamic",
#         key="data_editor"
#     )
#
#     # --- Map Section ---
#     st.subheader("🌍 Interactive Map")
#     m = folium.Map(location=[filtered_df["Latitude"].mean(), filtered_df["Longitude"].mean()], zoom_start=7, tiles="CartoDB positron")
#     marker_cluster = MarkerCluster().add_to(m)
#
#     # Generate color palette for category
#     color_cycle = itertools.cycle([
#         "red", "blue", "green", "purple", "orange", "darkred", "lightred",
#         "beige", "darkblue", "darkgreen", "cadetblue", "darkpurple",
#         "white", "pink", "lightblue", "lightgreen", "gray", "black"
#     ])
#
#     if category_column_key:
#         category_values = filtered_df[category_column_key].dropna().unique()
#         color_map = {val: next(color_cycle) for val in category_values}
#     else:
#         color_map = {}
#
#     # Plot points
#     for _, row in filtered_df.iterrows():
#         lat = row["Latitude"]
#         lon = row["Longitude"]
#         title = row.get("TITLE", "No Title")
#         state = row.get("STATE", "")
#         category_value = row.get(category_column_key, "") if category_column_key else ""
#         color = color_map.get(category_value, "blue")
#
#         popup_text = f"<b>{title}</b><br>State: {state}"
#         if category_column_key:
#             popup_text += f"<br>{selected_category}: {category_value}"
#
#         folium.Marker(
#             location=[lat, lon],
#             popup=folium.Popup(popup_text, max_width=300),
#             tooltip=popup_text,
#             icon=folium.Icon(color=color, icon="info-sign")
#         ).add_to(marker_cluster)
#
#     # Zoom to selected row
#     if not selected_row.empty:
#         lat = selected_row["Latitude"].values[0]
#         lon = selected_row["Longitude"].values[0]
#         m.location = [lat, lon]
#         m.zoom_start = 14
#
#     # Show map big
#     st_data = st_folium(m, width=1200, height=650)
#

# import streamlit as st
# import pandas as pd
# import numpy as np
# import folium
# from folium.plugins import MarkerCluster
# from streamlit_folium import st_folium
# import re
#
# st.set_page_config(layout="wide")
# st.title("🗺️ Map of Mineral Titles with Tooltips & Google Maps Links")
#
# uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx"])
#
#
# # --- Coordinate Parsing ---
# def dms_to_dd(deg, minutes, seconds, direction):
#     dd = float(deg) + float(minutes) / 60 + float(seconds) / 3600
#     if direction.upper() in ['S', 'W']:
#         dd *= -1
#     return dd
#
#
# def parse_coordinates(coord_str):
#     if pd.isna(coord_str):
#         return np.nan, np.nan
#
#     coord_str = coord_str.replace(',', ' ').replace('&', ' ')
#     coord_str = coord_str.replace('o', '°').replace('’', "'").replace('”', '"')
#     coord_str = coord_str.upper()
#
#     # Format: 4 52 15E, 6 53 45N
#     try:
#         pattern = re.findall(r'(\d+)\s+(\d+)\s+(\d+)\s*([NSEW])', coord_str)
#         if len(pattern) >= 2:
#             lon = dms_to_dd(*pattern[0])
#             lat = dms_to_dd(*pattern[1])
#             return lat, lon
#     except:
#         pass
#
#     # Format: N 07° 24' 41.5" E 005° 14' 32.2"
#     try:
#         pattern = re.findall(
#             r'([NS])\s*(\d+)[°O]?\s*(\d+)[\'′]\s*([\d.]+)["”]?\s*([EW])\s*(\d+)[°O]?\s*(\d+)[\'′]\s*([\d.]+)["”]?',
#             coord_str
#         )
#         if pattern:
#             lat_d, lat_m, lat_s = pattern[0][1], pattern[0][2], pattern[0][3]
#             lon_d, lon_m, lon_s = pattern[0][5], pattern[0][6], pattern[0][7]
#             lat = dms_to_dd(lat_d, lat_m, lat_s, pattern[0][0])
#             lon = dms_to_dd(lon_d, lon_m, lon_s, pattern[0][4])
#             return lat, lon
#     except:
#         pass
#
#     return np.nan, np.nan
#
#
# # --- Main App ---
# if uploaded_file:
#     df = pd.read_excel(uploaded_file)
#     coord_col = "GEOGRAPHICAL COORDINATES OF THE MINERAL TITLE ( LONG. & LAT)"
#
#     if coord_col not in df.columns:
#         st.error(f"Column '{coord_col}' not found in Excel file.")
#         st.stop()
#
#     df["Latitude"], df["Longitude"] = zip(*df[coord_col].apply(parse_coordinates))
#     valid_coords = df.dropna(subset=["Latitude", "Longitude"]).copy()
#
#     if valid_coords.empty:
#         st.warning("⚠️ No valid coordinates found for selected filters.")
#         st.dataframe(df)
#         st.stop()
#
#     # 🔗 Create Google Maps Link
#     valid_coords["Map Link"] = valid_coords.apply(
#         lambda row: f"https://www.google.com/maps?q={row['Latitude']},{row['Longitude']}", axis=1
#     )
#
#     # 🧼 Clean link to clickable markdown
#     valid_coords["Map Link"] = valid_coords["Map Link"].apply(
#         lambda x: f"[Open in Google Maps]({x})"
#     )
#
#     # 🔍 Search box
#     search_text = st.text_input("🔍 Search by any text (Title, State, etc):")
#     if search_text:
#         filtered_df = valid_coords[valid_coords.apply(
#             lambda row: search_text.lower() in str(row).lower(), axis=1
#         )]
#     else:
#         filtered_df = valid_coords
#
#     # 📋 Show table with clickable links
#     st.subheader("📄 Mineral Titles Table (Click a row to zoom on map)")
#     selected_row = st.data_editor(
#         filtered_df,
#         column_order=None,
#         hide_index=True,
#         use_container_width=True,
#         num_rows="dynamic",
#         key="data_editor"
#     )
#
#     # 🗺️ Map
#     m = folium.Map(location=[
#         filtered_df["Latitude"].mean(),
#         filtered_df["Longitude"].mean()
#     ], zoom_start=7, control_scale=True)
#
#     marker_cluster = MarkerCluster().add_to(m)
#
#     for _, row in filtered_df.iterrows():
#         title = row.get("TITLE", "")
#         state = row.get("STATE", "")
#         popup_html = f"<b>{title}</b><br>State: {state}<br><a href='https://www.google.com/maps?q={row['Latitude']},{row['Longitude']}' target='_blank'>Open in Google Maps</a>"
#
#         folium.Marker(
#             location=[row["Latitude"], row["Longitude"]],
#             popup=folium.Popup(popup_html, max_width=300),
#             tooltip=f"{title} ({state})",
#             icon=folium.Icon(color="blue", icon="map-pin", prefix="fa")
#         ).add_to(marker_cluster)
#
#     # 🔍 Zoom if row clicked
#     if not selected_row.empty:
#         lat = selected_row["Latitude"].values[0]
#         lon = selected_row["Longitude"].values[0]
#         m.location = [lat, lon]
#         m.zoom_start = 14
#
#     # 🖥️ Display Map (large)
#     st_data = st_folium(m, width=1200, height=600)
#
# import streamlit as st
# import pandas as pd
# import numpy as np
# import folium
# from folium.plugins import MarkerCluster
# from streamlit_folium import st_folium
# import re
#
# st.set_page_config(layout="wide")
# st.title("🗺️ Map of Mineral Titles with Tooltips and Google Maps Links")
#
#
# # --- Coordinate Parsing ---
# def dms_to_dd(deg, minutes, seconds, direction):
#     dd = float(deg) + float(minutes) / 60 + float(seconds) / 3600
#     if direction.upper() in ['S', 'W']:
#         dd *= -1
#     return dd
#
#
# def parse_coordinates(coord_str):
#     if pd.isna(coord_str):
#         return np.nan, np.nan
#
#     coord_str = coord_str.replace(',', ' ').replace('&', ' ')
#     coord_str = coord_str.replace('o', '°').replace('’', "'").replace('”', '"')
#     coord_str = coord_str.upper()
#
#     # Try DMS like "4 52 15E, 6 53 45N"
#     try:
#         pattern = re.findall(r'(\d+)\s+(\d+)\s+(\d+)\s*([NSEW])', coord_str)
#         if len(pattern) >= 2:
#             lon = dms_to_dd(*pattern[0])
#             lat = dms_to_dd(*pattern[1])
#             return lat, lon
#     except:
#         pass
#
#     # Try full fancy DMS like 'N 07° 24' 41.5" E 005° 14' 32.2"'
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
#
#     return np.nan, np.nan
#
#
# # --- App Logic ---
# uploaded_file = st.file_uploader("📁 Upload your Excel file", type=["xlsx"])
#
# if uploaded_file:
#     df = pd.read_excel(uploaded_file)
#     coord_col = "GEOGRAPHICAL COORDINATES OF THE MINERAL TITLE ( LONG. & LAT)"
#
#     if coord_col not in df.columns:
#         st.error(f"Column '{coord_col}' not found in Excel file.")
#         st.stop()
#
#     # Parse coordinates
#     df["Latitude"], df["Longitude"] = zip(*df[coord_col].apply(parse_coordinates))
#
#     # Drop invalid rows
#     valid_coords = df.dropna(subset=["Latitude", "Longitude"]).copy()
#
#     if valid_coords.empty:
#         st.warning("⚠️ No valid coordinates found.")
#         st.dataframe(df)
#         st.stop()
#
#     # Merge Lat/Lon into Google Maps link
#     valid_coords["📍 Coordinates"] = valid_coords.apply(
#         lambda
#             row: f'<a href="https://www.google.com/maps?q={row["Latitude"]},{row["Longitude"]}" target="_blank">📍 View on Map</a>',
#         axis=1
#     )
#
#     # --- Search Filter ---
#     search_text = st.text_input("🔍 Search by Title, State, or anything:")
#     if search_text:
#         filtered_df = valid_coords[valid_coords.apply(lambda row: search_text.lower() in str(row).lower(), axis=1)]
#     else:
#         filtered_df = valid_coords
#
#     st.markdown("### 📄 Mineral Titles Table (with Google Maps Link)")
#     st.write(filtered_df.to_html(escape=False, index=False), unsafe_allow_html=True)
#
#     # --- Map Section ---
#     st.markdown("### 🗺️ Map View")
#     m = folium.Map(location=[filtered_df["Latitude"].mean(), filtered_df["Longitude"].mean()], zoom_start=8,
#                    control_scale=True)
#     marker_cluster = MarkerCluster().add_to(m)
#
#     # Color legend setup
#     color_palette = ['red', 'green', 'blue', 'purple', 'orange', 'darkred', 'lightgray']
#     category_column = "ACTIVITY" if "ACTIVITY" in filtered_df.columns else None
#     unique_categories = filtered_df[category_column].unique().tolist() if category_column else []
#     category_color_map = {cat: color_palette[i % len(color_palette)] for i, cat in enumerate(unique_categories)}
#
#     for _, row in filtered_df.iterrows():
#         lat, lon = row["Latitude"], row["Longitude"]
#         title = row.get("TITLE", "No Title")
#         state = row.get("STATE", "")
#         activity = row.get(category_column, "Other") if category_column else "Other"
#         color = category_color_map.get(activity, "gray")
#
#         popup_text = f"<b>{title}</b><br>State: {state}<br>Activity: {activity}"
#         folium.Marker(
#             location=[lat, lon],
#             popup=popup_text,
#             tooltip=title,
#             icon=folium.Icon(color=color, icon="info-sign")
#         ).add_to(marker_cluster)
#
#     # Display enlarged map
#     st_data = st_folium(m, width=1200, height=600)

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
local_excel_path = r"C:\Users\dell\Downloads\Active _Operational Mineral Tiles.xlsx"  # 👉 Update this path as needed

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
