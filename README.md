# CASSINI Hackathon - Farm IQ

## Overview

Farm IQ is an agriculture expert system designed to help farmers optimize their yield and mitigate the impact of climate instability. By analyzing historical and forecasted weather data, along with satellite and NDVI information, it provides tailored recommendations on crop selection, sowing, watering, and harvesting.

## Features

- **Weather Data Analysis:** Fetches historical and forecasted meteorological data.
- **NDVI Calculation:** Uses satellite imagery to calculate NDVI for monitoring crop health.
- **Plot Information:** Provides detailed information about specific plots.
- **Interactive Maps:** Displays plot boundaries and relevant data on interactive maps.

## EU Space Technologies

Farm IQ leverages satellite data (Copernicus) and NDVI for monitoring soil health, crop growth, and forecasting climate conditions. This data enables precise insights to guide farming decisions, boosting sustainability and efficiency.

## Space for Environment & Green Transition

Farm IQ addresses the challenge of climate change adaptation in agriculture. It supports sustainable farming practices by minimizing water usage and optimizing crop yield, contributing to a greener economic system.

## How to Run

1. **Clone the Repository:**
    ```sh
    git clone https://github.com/geoah/cassini-farmiq.git
    cd cassini-farmiq
    ```

2. **Install Dependencies:**
    Ensure you have [Poetry](https://python-poetry.org/) installed, then run:
    ```sh
    poetry install
    ```

3. **Set Up Earth Engine:**
    Follow the instructions to set up [Google Earth Engine](https://developers.google.com/earth-engine/guides/python_install).

4. **Run the Streamlit App:**
    ```sh
    poetry run streamlit run farm.py
    ```

5. **Access the App:**
    Open your web browser and go to `http://localhost:8501`.

## Configuration

- **Plot Data:** Ensure `farm-plot.txt` contains the necessary plot data.
- **Environment Variables:** Set up any required environment variables for accessing APIs and services.
    - **OpenAI API Key:** Set the `OPENAI_API_KEY` environment variable to your OpenAI API key.
    - **Google Earth Engine API Key:** Configure Google Earth Engine API key using the `gcloud` CLI.