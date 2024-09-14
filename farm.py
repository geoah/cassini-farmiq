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


# Helper function to get bounding box from plot_id
def get_bounding_box(plot_id: str) -> tuple:
    # For this POC, always return the same bounding box
    return (40.712, -74.006, 40.713, -74.005)

@openai_function(descriptions={
    "plot_id": "The identifier of the plot.",
    "start_date": "Start date for the satellite data in YYYY-MM-DD format.",
    "end_date": "End date in YYYY-MM-DD format.",
    "image_collection": "The satellite image collection to retrieve data from (e.g., 'COPERNICUS/S2')."
})
def fetch_satellite_timeline(plot_id: str, start_date: str, end_date: str, image_collection: str) -> str:
    bbox = get_bounding_box(plot_id)
    response = (
        f"Satellite data for plot {plot_id} (bbox: {bbox}) from {start_date} to {end_date} using {image_collection}:\n"
        " - 2023-05-01: Satellite data point 1\n"
        " - 2023-05-02: Satellite data point 2\n"
    )
    print(f"Fetching satellite timeline for plot {plot_id} from {start_date} to {end_date} using {image_collection}")
    return response

@openai_function(descriptions={
    "plot_id": "The identifier of the plot."
})
def fetch_plot_data(plot_id: str) -> str:
    bbox = get_bounding_box(plot_id)
    if plot_id == "Plot123":
        response = (
            f"Plot Data for {plot_id}:\n"
            f"Bounding Box: {bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}\n"
            "Seasons:\n"
            " - Year: 2021, Crop: corn\n"
            "   - 2021-03-15: Sowing (Seed Type: Hybrid A, Quantity: 100kg)\n"
            "   - 2021-03-25: Germination (Percentage Germinated: 95%, Time: 10 days)\n"
            "   - 2021-04-10: Seedling Development (Height: 15cm, Number of Leaves: 4)\n"
            "   - 2021-05-05: Vegetative Growth (Biomass: 200kg/ha, Height: 1m, Leaf Area: 0.5m²)\n"
            "   - 2021-06-01: Flowering (Number of Flowers: 500, Time: 75 days)\n"
            "   - 2021-06-15: Pollination (Success Rate: 90%)\n"
            "   - 2021-06-25: Fruit Setting (Number of Fruits: 450, Size: Medium)\n"
            "   - 2021-07-05: Maturation (Fruit Size: Large, Color: Yellow, Nutrient Content: High)\n"
            "   - 2021-07-10: Harvest (Weight: 10 tons, Yield: 8 tons/ha, Quality: Excellent)\n"
            " - Year: 2022, Crop: corn\n"
            "   - 2022-03-12: Sowing (Seed Type: Hybrid B, Quantity: 110kg)\n"
            "   - 2022-03-22: Germination (Percentage Germinated: 93%, Time: 10 days)\n"
            "   - 2022-04-08: Seedling Development (Height: 14cm, Number of Leaves: 3)\n"
            "   - 2022-05-03: Vegetative Growth (Biomass: 190kg/ha, Height: 0.9m, Leaf Area: 0.45m²)\n"
            "   - 2022-05-28: Flowering (Number of Flowers: 480, Time: 76 days)\n"
            "   - 2022-06-12: Pollination (Success Rate: 88%)\n"
            "   - 2022-06-22: Fruit Setting (Number of Fruits: 422, Size: Medium)\n"
            "   - 2022-07-02: Maturation (Fruit Size: Large, Color: Yellow, Nutrient Content: High)\n"
            "   - 2022-07-15: Harvest (Weight: 9.5 tons, Yield: 7.8 tons/ha, Quality: Good)\n"
            " - Year: 2023, Crop: corn\n"
            "   - 2023-03-18: Sowing (Seed Type: Hybrid C, Quantity: 105kg)\n"
            "   - 2023-03-28: Germination (Percentage Germinated: 96%, Time: 10 days)\n"
            "   - 2023-04-13: Seedling Development (Height: 16cm, Number of Leaves: 4)\n"
            "   - 2023-05-08: Vegetative Growth (Biomass: 210kg/ha, Height: 1.1m, Leaf Area: 0.55m²)\n"
            "   - 2023-06-03: Flowering (Number of Flowers: 510, Time: 75 days)\n"
            "   - 2023-06-18: Pollination (Success Rate: 92%)\n"
            "   - 2023-06-28: Fruit Setting (Number of Fruits: 470, Size: Large)\n"
            "   - 2023-07-08: Maturation (Fruit Size: Extra Large, Color: Golden, Nutrient Content: Very High)\n"
            "   - 2023-07-20: Harvest (Weight: 10.5 tons, Yield: 8.5 tons/ha, Quality: Excellent)\n"
        )
    else:
        response = f"No data available for plot {plot_id}."
    print(f"Fetching plot data for plot_id {plot_id}")
    return response

@openai_function(descriptions={
    "plot_id": "The identifier of the plot."
})
def calculate_nvdi(plot_id: str) -> str:
    bbox = get_bounding_box(plot_id)
    response = f"Calculated NVDI values for plot {plot_id} (bbox: {bbox}): 0.65, 0.70, 0.75"
    print(f"Calculating NVDI for plot {plot_id}")
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
    ndvi_df = ndvi_df.sort_values('date')

    # Calculate mean NDVI
    mean_ndvi = ndvi_df['NDVI'].mean()

    # Create the response string
    response = f"NDVI data for plot {plot_id} from {start_date} to {end_date}:\n"
    response += f"Mean NDVI: {mean_ndvi:.4f}\n"
    response += "NDVI graph has been generated and can be displayed in the Streamlit app."

    # Store the DataFrame in the session state for later display
    st.session_state['ndvi_data'] = ndvi_df

    return response

# Create the assistant
ass = Assistant.create(
    name="Farm Perfect Assistant",
    instructions=(
        "You are Farm Perfect, an agriculture expert system that helps farmers optimize crop yield and "
        "prevent diseases by analyzing historical and predicted data. The user will provide the plot's ID with their message. "
        "Use this plot ID to retrieve data for that specific plot using the tools available. "
        "Explain what data you requested, the calculations you performed, and present a helpful response."
    ),
    functions=[
        fetch_satellite_timeline,
        fetch_plot_data,
        calculate_nvdi,
        fetch_meteo_timeline,
        fetch_meteo_forecast_timeline,
        fetch_ndvi_data
    ]
)

# Create a conversation
conversation = ass.conversation.create()

# Start the Streamlit app

st.title("Farm Perfect Assistant")

# Input for plot ID
plot_id = st.text_input("Plot ID:", value="Plot123")

# Fetch plot data
plot_data_str = fetch_plot_data(plot_id)

# Display map with plot boundaries
st.subheader("Plot Location")

# Extract bounding box from plot data
bbox_match = re.search(r'Bounding Box: ([\d\.,-]+)', plot_data_str)
if bbox_match:
    bbox_str = bbox_match.group(1)
    bbox_values = [float(x.strip()) for x in bbox_str.split(',')]
    
    # Create a folium map
    m = folium.Map(location=[(bbox_values[0] + bbox_values[2]) / 2, (bbox_values[1] + bbox_values[3]) / 2], 
                   zoom_start=18,  # Increased zoom level for smaller area
                   tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                   attr="Esri")
    
    # Add polygon to the map
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
    
    # Display the map
    folium_static(m)

# Display plot information
st.subheader("Plot Information")
st.text(plot_data_str)

# Text input for user query
user_input = st.text_input("Ask the assistant:")

if user_input:
    user_input_with_plot_id = f"Plot ID: {plot_id}\n{user_input}"
    # Use streaming
    stream = conversation.ask_stream(user_input_with_plot_id)
    response_placeholder = st.empty()
    full_response = ""
    for event in stream:
        full_response += event.text
        response_placeholder.write(full_response)
    
    # Check if temperature data was fetched and display the graph
    if 'temperature_data' in st.session_state:
        st.subheader("Temperature Data")
        temperature_data = st.session_state['temperature_data']
        st.line_chart(temperature_data)
        # Clear the temperature data from session state
        del st.session_state['temperature_data']
    
    # Check if NDVI data was generated and display the graph
    if 'ndvi_data' in st.session_state:
        st.subheader("NDVI Data")
        ndvi_data = st.session_state['ndvi_data']
        fig, ax = plt.subplots()
        ax.plot(ndvi_data['date'], ndvi_data['NDVI'])
        ax.set_xlabel('Date')
        ax.set_ylabel('NDVI')
        ax.set_title('NDVI Over Time')
        st.pyplot(fig)
        # Clear the NDVI data from session state
        del st.session_state['ndvi_data']