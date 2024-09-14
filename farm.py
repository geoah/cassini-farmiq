import streamlit as st
import random
import pandas as pd
import datetime
from ez_openai import Assistant, openai_function
import pydeck as pdk
import re

# Define the tools/functions with plot_id and string inputs for bounding_box and types

@openai_function(descriptions={
    "plot_id": "The identifier of the plot.",
    "start_date": "Start date for the satellite data in YYYY-MM-DD format.",
    "end_date": "End date in YYYY-MM-DD format.",
    "image_collection": "The satellite image collection to retrieve data from (e.g., 'COPERNICUS/S2')."
})
def fetch_satellite_timeline(plot_id: str, start_date: str, end_date: str, image_collection: str) -> str:
    # For demo purposes, return a human-readable string
    response = (
        f"Satellite data for plot {plot_id} from {start_date} to {end_date} using {image_collection}:\n"
        " - 2023-05-01: Satellite data point 1\n"
        " - 2023-05-02: Satellite data point 2\n"
    )
    print(f"Fetching satellite timeline for plot {plot_id} from {start_date} to {end_date} using {image_collection}")
    return response

@openai_function(descriptions={
    "plot_id": "The identifier of the plot."
})
def fetch_plot_data(plot_id: str) -> str:
    if plot_id == "Plot123":
        response = (
            f"Plot Data for {plot_id}:\n"
            "Bounding Box: 40.9,23.0,41.0,23.1\n"
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

@openai_function()
def calculate_nvdi() -> str:
    response = "Calculated NVDI values: 0.65, 0.70, 0.75"
    print("Calculating NVDI")
    return response

@openai_function(descriptions={
    "types": "Meteorological data types as a string of comma-separated values (e.g., 'temperature,precipitation').",
    "bounding_box": "The bounding box of the area as a string of comma-separated floats.",
    "start_date": "Start date in YYYY-MM-DD format.",
    "end_date": "End date in YYYY-MM-DD format."
})
def fetch_meteo_timeline(types: str, bounding_box: str, start_date: str, end_date: str) -> str:
    types_list = [t.strip() for t in types.split(',')]
    start_date_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
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
        st.session_state['temperature_data'] = data
    response_lines = [f"Meteorological data for types {', '.join(types_list)} from {start_date} to {end_date}:"]
    for entry in data:
        line = f" - {entry['date']}: " + ", ".join([f"{key.capitalize()}: {value}" for key, value in entry.items() if key != 'date'])
        response_lines.append(line)
    response = "\n".join(response_lines)
    print(f"Fetching meteorological data for types {types_list}, bounding box {bounding_box} from {start_date} to {end_date}")
    return response

@openai_function(descriptions={
    "types": "Meteorological data types as a string of comma-separated values (e.g., 'temperature,precipitation').",
    "bounding_box": "The bounding box of the area as a string of comma-separated floats.",
    "start_date": "Start date in YYYY-MM-DD format.",
    "end_date": "End date in YYYY-MM-DD format."
})
def fetch_meteo_forecast_timeline(types: str, bounding_box: str, start_date: str, end_date: str) -> str:
    types_list = [t.strip() for t in types.split(',')]
    start_date_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
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
        st.session_state['temperature_data'] = data
    response_lines = [f"Meteorological forecast for types {', '.join(types_list)} from {start_date} to {end_date}:"]
    for entry in data:
        line = f" - {entry['date']}: " + ", ".join([f"{key.capitalize()}: {value}" for key, value in entry.items() if key != 'date'])
        response_lines.append(line)
    response = "\n".join(response_lines)
    print(f"Fetching meteorological forecast data for types {types_list}, bounding box {bounding_box} from {start_date} to {end_date}")
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
        fetch_meteo_forecast_timeline
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
    # Create polygon data
    polygon = [[bbox_values[1], bbox_values[0]],
               [bbox_values[3], bbox_values[0]],
               [bbox_values[3], bbox_values[2]],
               [bbox_values[1], bbox_values[2]],
               [bbox_values[1], bbox_values[0]]]
    polygon_layer = pdk.Layer(
        "PolygonLayer",
        data=[{"polygon": polygon}],
        get_polygon="polygon",
        get_fill_color=[0, 0, 0, 0],  # Transparent fill
        get_line_color=[255, 0, 0],   # Red outline
        get_line_width=2,
        pickable=True,
        stroked=True,
        filled=False
    )
    view_state = pdk.ViewState(
        longitude=(bbox_values[1] + bbox_values[3]) / 2,
        latitude=(bbox_values[0] + bbox_values[2]) / 2,
        zoom=12
    )
    r = pdk.Deck(layers=[polygon_layer], initial_view_state=view_state)
    st.pydeck_chart(r)

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
        df = pd.DataFrame(temperature_data)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        if 'temperature' in df.columns:
            st.line_chart(df['temperature'])
        # Clear the temperature data from session state
        del st.session_state['temperature_data']
