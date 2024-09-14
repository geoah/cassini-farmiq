# Use Python 3.10-slim as the base image
FROM python:3.10-slim

# Install system dependencies for GDAL, GEOS, and PostgreSQL/PostGIS
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    postgresql-client \
    gcc \
    g++ \
    python3-dev \
    musl-dev \
    curl

# Downloading gcloud package
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz

# Installing the package
RUN mkdir -p /usr/local/gcloud \
  && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
  && /usr/local/gcloud/google-cloud-sdk/install.sh

# Adding the package path to local
ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

# Set working directory inside the container
WORKDIR /app

# Copy pyproject.toml and poetry.lock (or requirements.txt if using pip)
COPY pyproject.toml poetry.lock ./

# Create the directory for Earth Engine credentials
RUN mkdir -p /root/.config/earthengine/

# Copy the Earth Engine credentials file
COPY .config-earthengine-credentials /root/.config/earthengine/

# Install Poetry or pip dependencies
RUN pip install poetry
RUN poetry config virtualenvs.create false \
    && poetry lock && poetry install --no-interaction --no-ansi

# Copy the rest of the application code
COPY . .

# Expose port 8000
EXPOSE 8000

# Default command to run the app
CMD ["python", "farm_perfect/manage.py", "runserver", "0.0.0.0:8000"]
