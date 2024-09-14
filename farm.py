import streamlit as st
import random
import pandas as pd
import datetime
from ez_openai import Assistant, openai_function
import folium
from streamlit_folium import folium_static
import re
from meteostat import Point, Daily
from datetime import datetime
import ee
import matplotlib.pyplot as plt

# Initialize Earth Engine
ee.Initialize()

# Load plot data from TXT file
with open('farm-plot.txt', 'r') as file:
    PLOT123_DATA = file.read()

# Helper function to get bounding box from plot_id
def get_bounding_box(plot_id: str) -> tuple:
    # For this POC, always return the same bounding box
    return (40.712, -74.006, 40.713, -74.005)

@openai_function(descriptions={
    "plot_id": "The identifier of the plot."
})
def fetch_plot_data(plot_id: str) -> str:
    bbox = get_bounding_box(plot_id)
    if plot_id == "Plot123":
        response = (
            f"Plot Data for {plot_id}:\n"
            f"Bounding Box: {bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}\n"
            f"{PLOT123_DATA}"
        )
    else:
        response = f"No data available for plot {plot_id}."
    print(f"Fetching plot data for plot_id {plot_id}")
    return response

@openai_function(descriptions={
    "plot_id": "The identifier of the plot.",
    "types": "Meteorological data types as a string of comma-separated values (e.g., 'temperature,precipitation').",
    "start_date": "Start date in YYYY-MM-DD format.",
    "end_date": "End date in YYYY-MM-DD format."
})
def fetch_meteo_timeline(plot_id: str, types: str, start_date: str, end_date: str) -> str:
    types_list = [t.strip() for t in types.split(',')]
    bbox = get_bounding_box(plot_id)
    
    # Use the center of the bounding box for the weather data
    lat = (bbox[0] + bbox[2]) / 2
    lon = (bbox[1] + bbox[3]) / 2
    
    # Create Point for the location
    location = Point(lat, lon)
    
    # Convert string dates to datetime objects
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Fetch data
    data = Daily(location, start, end)
    data = data.fetch()
    
    # Prepare response
    response_lines = [f"Meteorological data for plot {plot_id} (bbox: {bbox}), types {', '.join(types_list)} from {start_date} to {end_date}:"]
    
    for date, row in data.iterrows():
        line_parts = [f" - {date.strftime('%Y-%m-%d')}:"]
        if 'temperature' in types_list and 'tavg' in row:
            line_parts.append(f"Temperature: {row['tavg']:.1f}°C")
        if 'precipitation' in types_list and 'prcp' in row:
            line_parts.append(f"Precipitation: {row['prcp']:.1f}mm")
        if 'wind_speed' in types_list and 'wspd' in row:
            line_parts.append(f"Wind Speed: {row['wspd']:.1f}km/h")
        response_lines.append(" ".join(line_parts))
    
    response = "\n".join(response_lines)

    print(f"Fetched meteorological data for plot {plot_id}, types {types_list} from {start_date} to {end_date}")
    print("")
    print(data)
    print("-----")
    print("")
    
    # Store temperature data in session state if temperature is in types_list
    if 'temperature' in types_list:
        st.session_state['temperature_data'] = data['tavg'].to_frame()
    
    return response

@openai_function(descriptions={
    "plot_id": "The identifier of the plot.",
    "types": "Meteorological data types as a string of comma-separated values (e.g., 'temperature,precipitation').",
    "start_date": "Start date in YYYY-MM-DD format.",
    "end_date": "End date in YYYY-MM-DD format."
})
def fetch_meteo_forecast_timeline(plot_id: str, types: str, start_date: str, end_date: str) -> str:
    bbox = get_bounding_box(plot_id)
    types_list = [t.strip() for t in types.split(',')]
    start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
    delta = (end_date_dt - start_date_dt).days + 1
    dates = [start_date_dt + datetime.timedelta(days=i) for i in range(delta)]
    data = []
    for date in dates:
        day_data = {"date": date.strftime("%Y-%m-%d")}
        if 'temperature' in types_list:
            day_data['temperature'] = round(random.uniform(10, 35), 1)  # Celsius
        if 'precipitation' in types_list:
            day_data['precipitation'] = round(random.uniform(0, 20), 1)  # mm
        if 'wind_speed' in types_list:
            day_data['wind_speed'] = round(random.uniform(0, 15), 1)  # m/s
        data.append(day_data)
    # Store temperature data in session state if temperature is in types_list
    if 'temperature' in types_list:
        st.session_state['temperature_data'] = pd.DataFrame(data).set_index('date')['temperature']
    response_lines = [f"Meteorological forecast for plot {plot_id} (bbox: {bbox}), types {', '.join(types_list)} from {start_date} to {end_date}:"]
    for entry in data:
        line = f" - {entry['date']}: " + ", ".join([f"{key.capitalize()}: {value}" for key, value in entry.items() if key != 'date'])
        response_lines.append(line)
    response = "\n".join(response_lines)
    print(f"Fetching meteorological forecast data for plot {plot_id}, types {types_list} from {start_date} to {end_date}")
    return response

@openai_function(descriptions={
    "plot_id": "The identifier of the plot.",
    "start_date": "Start date for NDVI calculation in YYYY-MM-DD format.",
    "end_date": "End date for NDVI calculation in YYYY-MM-DD format."
})
def fetch_ndvi_data(plot_id: str, start_date: str, end_date: str) -> str:
    bbox = get_bounding_box(plot_id)
    
    # Create an Earth Engine geometry from the bounding box
    geometry = ee.Geometry.Rectangle([bbox[1], bbox[0], bbox[3], bbox[2]])
    
    # Get the Sentinel-2 image collection using the updated COPERNICUS/S2_SR_HARMONIZED dataset
    s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
        .filterBounds(geometry) \
        .filterDate(start_date, end_date) \
        .sort('CLOUDY_PIXEL_PERCENTAGE')

    # Function to calculate NDVI
    def addNDVI(image):
        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
        return image.addBands(ndvi)

    # Map the NDVI function over the image collection
    s2_with_ndvi = s2.map(addNDVI)

    # Function to extract NDVI values
    def extractNDVI(image):
        date = ee.Date(image.get('system:time_start')).format('YYYY-MM-dd')
        ndvi = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geometry,
            scale=10
        ).get('NDVI')
        return ee.Feature(None, {'date': date, 'NDVI': ndvi})

    # Extract NDVI values
    ndvi_values = s2_with_ndvi.map(extractNDVI).getInfo()

    # Convert to pandas DataFrame
    ndvi_df = pd.DataFrame([
        {'date': feature['properties']['date'], 'NDVI': feature['properties']['NDVI']}
        for feature in ndvi_values['features']
    ])
    ndvi_df['date'] = pd.to_datetime(ndvi_df['date'])
    ndvi_df = ndvi_df.sort_values('date').set_index('date')

    # Calculate mean NDVI
    mean_ndvi = ndvi_df['NDVI'].mean()

    # Create the response string
    response = f"NDVI data for plot {plot_id} from {start_date} to {end_date}:\n"
    response += f"Mean NDVI: {mean_ndvi:.4f}\n"
    response += "NDVI graph has been generated and can be displayed in the Streamlit app."

    # Store the DataFrame in the session state for later display
    st.session_state['ndvi_data'] = ndvi_df

    print(f"Fetching NDVI data for plot {plot_id} from {start_date} to {end_date}")
    print(ndvi_df)
    print("-----")
    print("")

    return response

# Create the assistant
ass = Assistant.create(
    name="Farm Perfect Assistant",
    instructions=(
        "You are Farm Perfect, an agriculture expert system that helps farmers optimize crop yield "
        "by analyzing historical and predicted data. The user will provide the plot's ID with their message. "
        "Use the plot ID to retrieve data for that specific plot using the tools available."
        "Do not make up data, only use the data provided by the tools."
        "Do not return raw data, always return a summary of the data."
    ),
    functions=[
        fetch_plot_data,
        fetch_meteo_timeline,
        fetch_meteo_forecast_timeline,
        fetch_ndvi_data
    ]
)

# Create a conversation
conversation = ass.conversation.create()

# Streamlit app

st.title("Farm Perfect Assistant")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'plot_id' not in st.session_state:
    st.session_state.plot_id = None

# Function to display plot information
def display_plot_info(plot_id):
    plot_data_str = fetch_plot_data(plot_id)
    
    # Display map with plot boundaries
    st.subheader("Plot Location")
    bbox_match = re.search(r'Bounding Box: ([\d\.,-]+)', plot_data_str)
    if bbox_match:
        bbox_str = bbox_match.group(1)
        bbox_values = [float(x.strip()) for x in bbox_str.split(',')]
        
        m = folium.Map(location=[(bbox_values[0] + bbox_values[2]) / 2, (bbox_values[1] + bbox_values[3]) / 2], 
                       zoom_start=18,
                       tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                       attr="Esri")
        
        folium.Polygon(
            locations=[
                [bbox_values[0], bbox_values[1]],
                [bbox_values[2], bbox_values[1]],
                [bbox_values[2], bbox_values[3]],
                [bbox_values[0], bbox_values[3]]
            ],
            color="red",
            fill=False,
        ).add_to(m)
        
        folium_static(m)

    # Display plot information
    st.subheader("Plot Information")
    st.text(plot_data_str)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display graphs if available
        if message["role"] == "assistant":
            if 'temperature_data' in st.session_state:
                st.subheader("Temperature Data")
                st.line_chart(st.session_state.temperature_data)
                del st.session_state.temperature_data
            
            if 'ndvi_data' in st.session_state:
                st.subheader("NDVI Data")
                st.line_chart(st.session_state.ndvi_data)
                del st.session_state.ndvi_data

# Chat input
if prompt := st.chat_input("What would you like to know about the farm?"):
    if st.session_state.plot_id is None:
        # First message, set the plot ID
        st.session_state.plot_id = "Plot123"  # You can modify this to allow user input
        display_plot_info(st.session_state.plot_id)
        st.session_state.messages.append({"role": "assistant", "content": f"Plot ID set to: {st.session_state.plot_id}"})

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for event in conversation.ask_stream(f"Plot ID: {st.session_state.plot_id}\n{prompt}"):
            full_response += event.text
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Rerun to update the chat display
    st.rerun()

# Footer
st.markdown("---")
st.caption("Farm Perfect Assistant - Helping farmers optimize crop yield.")