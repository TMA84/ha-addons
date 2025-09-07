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

# Create config directory
mkdir -p /app/server/config

# Create configuration file
cat > /app/server/config/config.json << EOF
{
    "node-sonos-http-api": {
        "server": "${SONOS_SERVER}",
        "port": "${SONOS_PORT}",
        "rooms": ["${DEFAULT_ROOM}"]
    },
    "spotify": {
        "clientId": "${SPOTIFY_CLIENT_ID}",
        "clientSecret": "${SPOTIFY_CLIENT_SECRET}"
    },
    "clients": {}
}
EOF

# Create PIN file
cat > /app/server/config/pin.json << EOF
{
    "pin": "${ADMIN_PIN}"
}
EOF

# Create empty data file
echo "[]" > /app/server/config/data.json

bashio::log.info "Configuration created successfully"
bashio::log.info "Sonos Server: ${SONOS_SERVER}:${SONOS_PORT}"
bashio::log.info "Default Room: ${DEFAULT_ROOM}"

exec npm start