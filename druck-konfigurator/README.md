# Druck-Konfigurator (Home-Assistant-Add-on)

3D-Druck-Konfigurator für den **Anycubic Kobra S1** mit ACE: Druckwerte vorschlagen, 3MF für OrcaSlicer speichern,
Kosten mit exaktem Slicen (OrcaSlicer im Add-on), Slice-Vorschau, mehrere Platten mit Warteschlange,
Drucker-Werkbank (Kamera, Temperaturen, ACE) und Filamentverwaltung mit errechneter Restmenge.

Projekt und Handbuch: https://github.com/TMA84/druck-konfigurator

## Einrichten

1. Am Drucker den **LAN-Modus** einschalten (Einstellungen → Netzwerk).
2. Add-on installieren; unter **Konfiguration** die **Drucker-IP** (`printer_ip`) eintragen und starten.
   (Alternativ leer lassen und im Tool unter **⚙ Einstellungen → Drucker-Verbindung** eintragen.)
3. **Öffnen** bzw. in der Seitenleiste **Druck-Konfigurator**.

Das Image kommt fertig aus der GitHub Container Registry (`ghcr.io/tma84/ha-addon-druck-konfigurator-<arch>`,
gebaut von GitHub Actions) – die Installation lädt nur herunter.

Optional: Port **8765** in den Add-on-Einstellungen freigeben, dann ist das Tool auch direkt unter
`http://<Home-Assistant>:8765/` erreichbar (z. B. vom Tablet an der Werkbank).

## Daten

Spulen und Verbrauch der Filamentverwaltung liegen in `/data` des Add-ons und bleiben bei Updates erhalten.
Der Server zählt den Filamentverbrauch mit, solange das Add-on läuft – auch wenn die Seite geschlossen ist.

## Hinweise

- Architekturen: amd64 und aarch64 (z. B. Raspberry Pi 4/5). Das Image ist wegen OrcaSlicer rund 1,5 GB groß.
- Der Drucker muss aus Home Assistant erreichbar sein (gleiches Netz, private IP-Adresse).
- Lizenz: siehe Projekt; OrcaSlicer (AGPL-3.0) wird unverändert mitgeliefert.
