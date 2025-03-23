#!/usr/bin/with-contenv bashio

set +x

# Create main config
CLIENTID=$(bashio::config 'upstreamhost')
CLIENTSECRET=$(bashio::config 'upstreamport')
ROOM=$(bashio::config 'listenport')

echo "Preparing to run sonos-kids"
echo "CLIENTID: $CLIENTID"
echo "CLIENTSECRET: $CLIENTSECRET"
echo "ROOM: $ROOM"

sed -i "s/__CLIENTID__/${CLIENTID}/g" /app/Sonos-Kids-Controller/server/config/config.json
sed -i "s/__CLIENTSECRET__/${CLIENTSECRET}/g" /app/Sonos-Kids-Controller/server/config/config.json 
sed -i "s/__ROOM__/${ROOM}/g" /app/Sonos-Kids-Controller/server/config/config.json

echo "Generated Config"
cat /app/Sonos-Kids-Controller/server/config/ 

npm start