#!/bin/sh
# Start des Druck-Konfigurators im Add-on. Optionen aus /data/options.json (Home Assistant):
#   printer_ip   – IP-Adresse des Kobra S1 (LAN-Modus); die Seite übernimmt sie, die Filamentverwaltung zählt ab dem Start.
#   access_pin   – PIN für den direkten Zugriff über Port 8765 (leer = kein Schutz); Ingress schützt Home Assistant.
#   mqtt_control – Knöpfe „Druck pausieren/fortsetzen“ in Home Assistant (Standard aus; nie Abbrechen).
#   mqtt_enabled – Stand an Home Assistant über MQTT (Discovery). Zugangsdaten zum Broker (z. B. Mosquitto-Add-on)
#                  holt das Skript vom Supervisor (services: mqtt:want); ohne MQTT-Add-on bleibt MQTT einfach aus.
# Daten der Filamentverwaltung und der Warteschlange in /data (bleibt bei Updates erhalten).
set -e
mkdir -p /data
MQTT_ENABLED=true
if [ -f /data/options.json ]; then
  KONFIGURATOR_PRINTER=$(python3 -c "import json; print((json.load(open('/data/options.json')).get('printer_ip') or '').strip())")
  export KONFIGURATOR_PRINTER
  KONFIGURATOR_PIN=$(python3 -c "import json; print((json.load(open('/data/options.json')).get('access_pin') or '').strip())" || true)
  if [ -n "$KONFIGURATOR_PIN" ]; then
    export KONFIGURATOR_PIN
    echo "Zugriffsschutz: PIN für den direkten Port 8765 aktiv"
  else
    unset KONFIGURATOR_PIN
  fi
  MQTT_ENABLED=$(python3 -c "import json; print('false' if json.load(open('/data/options.json')).get('mqtt_enabled') is False else 'true')" || echo true)
  MQTT_CONTROL=$(python3 -c "import json; print('true' if json.load(open('/data/options.json')).get('mqtt_control') is True else 'false')" || echo false)
  export MQTT_CONTROL
  if [ "$MQTT_CONTROL" = "true" ]; then echo "Home Assistant darf Drucke pausieren und fortsetzen"; fi
fi

# MQTT: Zugangsdaten vom Supervisor ({data: {host, port, username, password, ssl}}). Fehler dürfen den Start nie verhindern.
if [ "$MQTT_ENABLED" = "true" ] && [ -n "$SUPERVISOR_TOKEN" ]; then
  MQTT_ENV=$(curl -s --max-time 10 -H "Authorization: Bearer $SUPERVISOR_TOKEN" http://supervisor/services/mqtt 2>/dev/null | python3 -c "
import json, shlex, sys
try:
    d = json.load(sys.stdin).get('data') or {}
except ValueError:
    d = {}
if d.get('host'):
    env = {'MQTT_HOST': d['host'], 'MQTT_PORT': d.get('port') or 1883, 'MQTT_USER': d.get('username') or '',
           'MQTT_PASSWORD': d.get('password') or '', 'MQTT_TLS': 'true' if d.get('ssl') else 'false'}
    print('\n'.join('%s=%s' % (k, shlex.quote(str(v))) for k, v in env.items()))
" 2>/dev/null || true)
  if [ -n "$MQTT_ENV" ]; then
    eval "$MQTT_ENV"
    export MQTT_HOST MQTT_PORT MQTT_USER MQTT_PASSWORD MQTT_TLS
    echo "MQTT: Broker $MQTT_HOST:$MQTT_PORT (vom Supervisor)"
  else
    echo "MQTT: kein MQTT-Broker gefunden (Mosquitto-Add-on installiert?) – Home-Assistant-Anbindung aus"
  fi
elif [ "$MQTT_ENABLED" != "true" ]; then
  echo "MQTT: in den Add-on-Einstellungen ausgeschaltet"
fi

# Dashboard-Karte „Druckwerkstatt 3D“ (custom:druckwerkstatt-card) nach /local/druckwerkstatt/ – Fehler verhindern den Start nie
if [ -d /homeassistant ] && [ -f /app/ha/druckwerkstatt-card.js ]; then
  if mkdir -p /homeassistant/www/druckwerkstatt 2>/dev/null && cp /app/ha/druckwerkstatt-card.js /homeassistant/www/druckwerkstatt/druckwerkstatt-card.js 2>/dev/null; then
    echo "Dashboard-Karte: /local/druckwerkstatt/druckwerkstatt-card.js"
  else
    echo "Dashboard-Karte: konnte nicht nach /homeassistant/www kopiert werden"
  fi
fi

echo "Druck-Konfigurator startet (Port 8765, Ingress)${KONFIGURATOR_PRINTER:+ – Drucker $KONFIGURATOR_PRINTER}"
cd /app
exec python tools/serve.py
