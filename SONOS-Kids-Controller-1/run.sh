#!/usr/bin/with-contenv bashio

set -e  # Exit on error

# Validate required config
CLIENTID=$(bashio::config 'clientid')
CLIENTSECRET=$(bashio::config 'clientsecret')
ROOM=$(bashio::config 'room')
SERVER=$(bashio::config 'apiserver')
PORT=$(bashio::config 'apiport')
DATA_FILE=$(bashio::config 'data')

# Validate required fields
if [[ -z "$CLIENTID" || -z "$CLIENTSECRET" || -z "$ROOM" ]]; then
    bashio::log.fatal "Missing required configuration: clientid, clientsecret, or room"
    exit 1
fi

bashio::log.info "Configuring Sonos Kids Controller..."
bashio::log.info "Room: $ROOM"
bashio::log.info "API Server: $SERVER:$PORT"

# Escape special characters for sed
CLIENTID_ESC=$(printf '%s\n' "$CLIENTID" | sed 's/[[\/.*^$()+?{|]/\\&/g')
CLIENTSECRET_ESC=$(printf '%s\n' "$CLIENTSECRET" | sed 's/[[\/.*^$()+?{|]/\\&/g')
ROOM_ESC=$(printf '%s\n' "$ROOM" | sed 's/[[\/.*^$()+?{|]/\\&/g')

# Update configuration
CONFIG_FILE="/app/Sonos-Kids-Controller/server/config/config.json"
sed -i "s/__CLIENTID__/${CLIENTID_ESC}/g" "$CONFIG_FILE"
sed -i "s/__CLIENTSECRET__/${CLIENTSECRET_ESC}/g" "$CONFIG_FILE"
sed -i "s/__ROOM__/${ROOM_ESC}/g" "$CONFIG_FILE"
sed -i "s/__SERVER__/${SERVER}/g" "$CONFIG_FILE"
sed -i "s/__PORT__/${PORT}/g" "$CONFIG_FILE"

# Link data file if provided
if [[ -n "$DATA_FILE" && -f "$DATA_FILE" ]]; then
    ln -sf "$DATA_FILE" /app/Sonos-Kids-Controller/server/config/data.json
    bashio::log.info "Data file linked successfully"
else
    bashio::log.warning "No data file provided or file not found"
fi

bashio::log.info "Starting Sonos Kids Controller..."
exec npm start