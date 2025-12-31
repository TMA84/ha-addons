#!/usr/bin/with-contenv bashio

set -e

# Get configuration
SPOTIFY_CLIENT_ID=$(bashio::config 'spotify_client_id')
SPOTIFY_CLIENT_SECRET=$(bashio::config 'spotify_client_secret')
SONOS_SERVER=$(bashio::config 'sonos_server')
SONOS_PORT=$(bashio::config 'sonos_port')
DEFAULT_ROOM=$(bashio::config 'default_room')
ADMIN_PIN=$(bashio::config 'admin_pin')

bashio::log.info "Starting Sonos Jukebox..."

# Create persistent data directory for SQLite database
mkdir -p /share/sonos-jukebox/data

# Link data directory to app for SQLite database
rm -rf /app/server/data
ln -sf /share/sonos-jukebox/data /app/server/data

# Configuration will be stored in SQLite database automatically
# No JSON config files needed - all config via database API

bashio::log.info "Configuration will be stored in SQLite database"
bashio::log.info "Sonos Server: ${SONOS_SERVER}:${SONOS_PORT}"
bashio::log.info "Default Room: ${DEFAULT_ROOM}"
bashio::log.info "Spotify Client ID: ${SPOTIFY_CLIENT_ID:0:10}..."
bashio::log.info "Database will be stored in: /share/sonos-jukebox/data/database.sqlite"

# Test network connectivity
bashio::log.info "Testing Sonos API connectivity..."
if curl -s --connect-timeout 5 "http://${SONOS_SERVER}:${SONOS_PORT}/zones" > /dev/null; then
    bashio::log.info "Sonos API is reachable"
else
    bashio::log.warning "Cannot reach Sonos API at ${SONOS_SERVER}:${SONOS_PORT}"
fi

# Set environment for server binding
export HOST=0.0.0.0
export PORT=8200

# Pass configuration as environment variables for initial setup
export SPOTIFY_CLIENT_ID="$SPOTIFY_CLIENT_ID"
export SPOTIFY_CLIENT_SECRET="$SPOTIFY_CLIENT_SECRET"
export SONOS_SERVER="$SONOS_SERVER"
export SONOS_PORT="$SONOS_PORT"
export DEFAULT_ROOM="$DEFAULT_ROOM"
export ADMIN_PIN="$ADMIN_PIN"

exec npm start