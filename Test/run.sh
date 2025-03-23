#!/usr/bin/with-contenv bashio

set +x

# Create main config
CLIENTID=$(bashio::config 'clientid')
CLIENTSECRET=$(bashio::config 'clientsecret')
ROOM=$(bashio::config 'room')
SERVER=$(bashio::config 'apiserver')
PORT=$(bashio::config 'apiport')

echo "Preparing to run sonos-kids"
echo "CLIENTID: $CLIENTID"
echo "CLIENTSECRET: $CLIENTSECRET"
echo "ROOM: $ROOM"

sed -i "s/__CLIENTID__/${CLIENTID}/g" /app/Sonos-Kids-Controller/server/config/config.json
sed -i "s/__CLIENTSECRET__/${CLIENTSECRET}/g" /app/Sonos-Kids-Controller/server/config/config.json 
sed -i "s/__ROOM__/${ROOM}/g" /app/Sonos-Kids-Controller/server/config/config.json
sed -i "s/__SERVER__/${SERVER}/g" /app/Sonos-Kids-Controller/server/config/config.json
sed -i "s/__PORT__/${PORT}/g" /app/Sonos-Kids-Controller/server/config/config.json

ln -s $(bashio::config 'data') /app/Sonos-Kids-Controller/server/config/data.json

echo "Generated Config"
cat /app/Sonos-Kids-Controller/server/config/config.json

echo "Data"
cat /app/Sonos-Kids-Controller/server/config/data.json

npm start