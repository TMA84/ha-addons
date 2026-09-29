#!/bin/sh
# Start des Druck-Konfigurators im Add-on. Optionen aus /data/options.json (Home Assistant):
#   printer_ip – IP-Adresse des Kobra S1 (LAN-Modus); die Seite übernimmt sie, die Filamentverwaltung zählt ab dem Start.
# Daten der Filamentverwaltung in /data (bleibt bei Updates erhalten).
set -e
mkdir -p /data
if [ -f /data/options.json ]; then
  KONFIGURATOR_PRINTER=$(python3 -c "import json; print((json.load(open('/data/options.json')).get('printer_ip') or '').strip())")
  export KONFIGURATOR_PRINTER
fi
echo "Druck-Konfigurator startet (Port 8765, Ingress)${KONFIGURATOR_PRINTER:+ – Drucker $KONFIGURATOR_PRINTER}"
cd /app
exec python tools/serve.py
