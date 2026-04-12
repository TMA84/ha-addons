#!/usr/bin/with-contenv bashio

# Get configuration
BRAND=$(bashio::config 'brand')

export BRAND

bashio::log.info "Starting Bluelink Token Generator..."
bashio::log.info "Brand: ${BRAND}"
bashio::log.info "Web UI available on port 9876"

# Activate virtual environment and run web server
source /opt/venv/bin/activate
exec python3 /app/web.py
