import streamlit as st
from ez_openai import Assistant, openai_function

# Define the tools/functions with string inputs for bounding_box and types

@openai_function(descriptions={
    "plot": "The plot identifier or bounding box as a string of comma-separated floats.",
    "start_date": "Start date for the satellite data in YYYY-MM-DD format.",
    "end_date": "End date for the satellite data in YYYY-MM-DD format.",
    "image_collection": "The satellite image collection to retrieve data from (e.g., 'COPERNICUS/S2')."
})
def fetch_satellite_timeline(plot: str, start_date: str, end_date: str, image_collection: str) -> str:
    """Retrieve satellite information for the given plot, start/end times, and image collection."""
    # For demo purposes, return a human-readable string
    response = (
        f"Satellite data for plot {plot} from {start_date} to {end_date} using {image_collection}:\n"
        " - 2023-05-01: Satellite data point 1\n"
        " - 2023-05-02: Satellite data point 2\n"
    )
    print(f"Fetching satellite timeline for plot {plot} from {start_date} to {end_date} using {image_collection}")
    return response

@openai_function()
def fetch_plot_data() -> str:
    """Returns the plot's data in a human-readable string format."""
    # Return updated dummy data as a string with detailed crop events
    response = (
        "Plot Data:\n"
        "Bounding Box: 35.0,-120.0,36.0,-119.0\n"
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
    print("Fetching plot data with detailed crop events")
    return response

@openai_function()
def calculate_nvdi() -> str:
    """Calculates NVDI and returns it as a string."""
    # Return dummy NVDI data as a string
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
    """Returns meteorological data as a string for given types, bounding box, and date range."""
    # Parse the types and bounding_box strings
    types_list = [t.strip() for t in types.split(',')]
    bbox_values = [float(x) for x in bounding_box.split(',')]
    print(f"Parsed types: {types_list}")
    print(f"Parsed bounding box: {bbox_values}")
    # Return dummy data as a string
    response = (
        f"Meteorological data for types {', '.join(types_list)} from {start_date} to {end_date}:\n"
        " - 2023-05-01: Temperature: 25°C, Precipitation: 0mm\n"
        " - 2023-05-02: Temperature: 26°C, Precipitation: 1mm\n"
    )
    print(f"Fetching meteorological data for types {types_list}, bounding box {bounding_box} from {start_date} to {end_date}")
    return response

@openai_function(descriptions={
    "types": "Meteorological data types as a string of comma-separated values (e.g., 'temperature,precipitation').",
    "bounding_box": "The bounding box of the area as a string of comma-separated floats.",
    "start_date": "Start date in YYYY-MM-DD format.",
    "end_date": "End date in YYYY-MM-DD format."
})
def fetch_meteo_forecast_timeline(types: str, bounding_box: str, start_date: str, end_date: str) -> str:
    """Returns meteorological forecast data as a string for given types, bounding box, and date range."""
    # Parse the types and bounding_box strings
    types_list = [t.strip() for t in types.split(',')]
    bbox_values = [float(x) for x in bounding_box.split(',')]
    print(f"Parsed types: {types_list}")
    print(f"Parsed bounding box: {bbox_values}")
    # Return dummy data as a string
    response = (
        f"Meteorological forecast for types {', '.join(types_list)} from {start_date} to {end_date}:\n"
        " - 2023-05-03: Temperature: 27°C, Precipitation: 0mm\n"
        " - 2023-05-04: Temperature: 28°C, Precipitation: 2mm\n"
    )
    print(f"Fetching meteorological forecast data for types {types_list}, bounding box {bounding_box} from {start_date} to {end_date}")
    return response

# Create the assistant
ass = Assistant.create(
    name="Farm Perfect Assistant",
    instructions=("""
You are **Farm Perfect**, an advanced agricultural assistant designed to help farmers optimize crop yields and combat diseases. Utilizing a combination of historical crop data and environmental predictions—including CO₂ levels, soil moisture, vegetation health, precipitation, and extreme weather events—you provide actionable insights and mitigation strategies.

When a farmer asks about a specific plot, you:

- **Understand the Question:** Carefully interpret the farmer's query to identify their needs.
- **Retrieve Data:** Use function calling and Retrieval-Augmented Generation (RAG) to gather relevant meteorological information, soil conditions, historical data about the plot, previous seasons, and harvests.
- **Analyze and Calculate:** Perform necessary calculations based on the retrieved data to generate insights.
- **Explain Your Process:** Clearly explain what data you requested and the calculations you performed.
- **Provide Recommendations:** Present a helpful and informative response that addresses the farmer's concerns and offers practical advice.

Your goal is to be a reliable and knowledgeable assistant, using the tools available to you to support farmers in making informed decisions about their crops.
"""),
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

# Fetch plot data
plot_data_str = fetch_plot_data()

# Display plot information
st.subheader("Plot Information")
st.text(plot_data_str)

# Text input for user query
user_input = st.text_input("Ask the assistant:")

if user_input:
    response = conversation.ask(user_input)
    st.subheader("Assistant's Response")
    st.write(response.text)
