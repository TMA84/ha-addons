#!/bin/sh
# Start des Druck-Konfigurators im Add-on. Daten der Filamentverwaltung in /data (bleibt bei Updates erhalten).
set -e
mkdir -p /data
echo "Druck-Konfigurator startet (Port 8765, Ingress) – Daten in /data"
cd /app
exec python tools/serve.py
