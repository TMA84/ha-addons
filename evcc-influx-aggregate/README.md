# EVCC Influx Aggregator Add-on

Aggregiert EVCC InfluxDB-Daten für die Grafana Dashboards von [ha-puzzles/evcc-grafana-dashboards](https://github.com/ha-puzzles/evcc-grafana-dashboards).

## Voraussetzungen

1. Eine laufende InfluxDB 1.8 Instanz mit EVCC-Daten
2. Eine separate Datenbank für die aggregierten Daten (empfohlen)

## Konfiguration

### InfluxDB Einstellungen

- **influx_evcc_db**: Name der EVCC InfluxDB (Standard: "evcc")
- **influx_evcc_user**: Benutzername der EVCC DB (leer wenn nicht benötigt)
- **influx_evcc_password**: Passwort der EVCC DB
- **influx_aggr_db**: Name der Aggregations-DB (Standard: "evcc_aggr")
- **influx_aggr_user**: Benutzername der Aggregations-DB
- **influx_aggr_password**: Passwort der Aggregations-DB
- **influx_host**: Hostname der InfluxDB (Standard: "localhost")
- **influx_port**: Port der InfluxDB (Standard: 8086)

### PV Konfiguration

- **peak_power_limit**: Limit in W um unrealistische Peaks zu filtern (Standard: 40000)
- **home_battery**: Hausbatterie vorhanden (Standard: true)
- **dynamic_tariff**: Dynamische Tarife erfassen (Standard: true)

### Allgemeine Einstellungen

- **timezone**: Zeitzone (Standard: "Europe/Berlin")
- **energy_sample_interval**: Abtastintervall für Energieberechnung (Standard: "60s")
- **tariff_price_interval**: Intervall der Tarifpreis-Updates (Standard: "15m")
- **cron_yesterday**: Cron-Ausdruck für gestrige Aggregation (Standard: "5 0 * * *")
- **cron_today**: Cron-Ausdruck für heutige Aggregation (Standard: "0 * * * *")
- **run_once**: Einmaliger Befehl beim Start (z.B. "--year 2024")
- **debug**: Debug-Ausgabe aktivieren (Standard: false)

## Einmalige Aggregation starten

Um z.B. ein ganzes Jahr zu aggregieren:

1. Setze `run_once` in der Addon-Konfiguration auf den gewünschten Befehl:
   - Ganzes Jahr: `--year 2024`
   - Einzelner Monat: `--month 2024 6`
   - Einzelner Tag: `--day 2024 7 16`
   - Datumsbereich: `--from 2023 3 6 --to 2025 2 15`
2. Starte das Addon neu
3. Der Befehl wird einmalig ausgeführt (kann je nach Datenmenge lange dauern)
4. Danach laufen die normalen Cron-Jobs weiter
5. Setze `run_once` wieder auf leer, damit der Befehl nicht bei jedem Neustart erneut ausgeführt wird

## Funktionsweise

1. Das Addon generiert die Konfigurationsdatei aus den HA-Einstellungen
2. Beim Start werden Fahrzeuge und Ladepunkte automatisch erkannt
3. Per Cron-Job werden die Daten regelmäßig aggregiert:
   - Jede Nacht um 00:05: Gestrige Daten
   - Jede volle Stunde: Heutige Daten

## Credits

Basiert auf [evcc-grafana-dashboards](https://github.com/ha-puzzles/evcc-grafana-dashboards) von ha-puzzles.
