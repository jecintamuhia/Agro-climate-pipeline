# Use official Python slim image with Debian base (better for geospatial deps)
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies required by geopandas, GDAL, PROJ, etc.
# These are needed at build time and runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgdal-dev \
    libproj-dev \
    libgeos-dev \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# If geopandas still complains about wheels → force source build (sometimes needed on slim)
# RUN pip install --no-cache-dir --no-binary :all: geopandas

# Copy the entire project code
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Healthcheck (optional but good practice)
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the Streamlit app
# --server.port=8501 --server.address=0.0.0.0 needed for Docker
CMD ["streamlit", "run", "dashboard/app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]