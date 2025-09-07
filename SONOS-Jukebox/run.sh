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

# Create persistent config directory
mkdir -p /config/sonos-jukebox

# Create or update configuration file
CONFIG_FILE="/config/sonos-jukebox/config.json"
if [[ ! -f "$CONFIG_FILE" ]]; then
    cat > "$CONFIG_FILE" << EOF
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
else
    # Update existing config with new values
    jq --arg server "$SONOS_SERVER" \
       --arg port "$SONOS_PORT" \
       --arg room "$DEFAULT_ROOM" \
       --arg clientId "$SPOTIFY_CLIENT_ID" \
       --arg clientSecret "$SPOTIFY_CLIENT_SECRET" \
       '."node-sonos-http-api".server = $server | 
        ."node-sonos-http-api".port = $port | 
        ."node-sonos-http-api".rooms = [$room] | 
        .spotify.clientId = $clientId | 
        .spotify.clientSecret = $clientSecret' \
       "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
fi

# Create PIN file if it doesn't exist
PIN_FILE="/config/sonos-jukebox/pin.json"
if [[ ! -f "$PIN_FILE" ]]; then
    cat > "$PIN_FILE" << EOF
{
    "pin": "${ADMIN_PIN}"
}
EOF
fi

# Create empty data file if it doesn't exist
DATA_FILE="/config/sonos-jukebox/data.json"
if [[ ! -f "$DATA_FILE" ]]; then
    echo "[]" > "$DATA_FILE"
fi

bashio::log.info "Configuration created successfully"
bashio::log.info "Sonos Server: ${SONOS_SERVER}:${SONOS_PORT}"
bashio::log.info "Default Room: ${DEFAULT_ROOM}"

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

exec npm start