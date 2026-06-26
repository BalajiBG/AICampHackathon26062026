# GARUDA AI - Intelligent Crime Intelligence Platform
# Optimized for Google Cloud Run
FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application files
COPY app.py .
COPY generate_crime_data.py .

# Generate synthetic crime database at build time
RUN python generate_crime_data.py

# Streamlit configuration
RUN mkdir -p /root/.streamlit
COPY streamlit_config.toml /root/.streamlit/config.toml

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8080/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
