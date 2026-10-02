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

**Zugriffs-PIN:** Der direkte Port hat ohne PIN keine Anmeldung – jeder im Heimnetz könnte Drucke starten. Unter
**Konfiguration → Zugriffs-PIN** (`access_pin`, 4–32 Zeichen) eine PIN setzen; dann fragt die Seite auf Port 8765
einmal danach (Anmeldung bleibt 30 Tage im Browser, nach einem Neustart des Add-ons neu anmelden; nach 5 falschen
Versuchen 5 Minuten Sperre). Die PIN schützt **nur den direkten Port** – über die Seitenleiste (Ingress) gibt es keine
PIN-Abfrage, dort schützt wie gehabt die Home-Assistant-Anmeldung. `/api/health` (Watchdog) bleibt ohne PIN erreichbar.

## Daten

Spulen und Verbrauch der Filamentverwaltung sowie die Druckwarteschlange liegen in `/data` des Add-ons und bleiben bei Updates erhalten.
Der Server zählt den Filamentverbrauch mit, solange das Add-on läuft – auch wenn die Seite geschlossen ist.

## Home Assistant (MQTT)

Mit einem MQTT-Broker (z. B. dem offiziellen **Mosquitto-Add-on**) meldet das Add-on den Stand als Gerät
**„Druck-Konfigurator <Druckermodell>“** an Home Assistant (MQTT-Discovery). Die Zugangsdaten holt es selbst vom
Supervisor; ausschalten lässt es sich unter **Konfiguration → Home Assistant (MQTT)** (`mqtt_enabled`).
Ohne Broker startet das Add-on ganz normal, nur ohne diese Entitäten. Über MQTT wird nichts gesteuert –
Drucke startest du weiter im Tool.

Die Warteschlange läuft auf dem Server: fertige Platten erkennt das Add-on auch, wenn keine Seite offen ist.

| Entität | Bedeutung |
|---|---|
| `sensor.druck_konfigurator_printer_state` | Druckerstatus (`frei`, `druckt`, `pausiert`, `fertig`, `abgebrochen`, `offline` …) |
| `sensor.druck_konfigurator_progress` | Fortschritt in % |
| `sensor.druck_konfigurator_remaining_min` | Restzeit des laufenden Drucks (min) |
| `sensor.druck_konfigurator_finish` | Fertig um (Zeitpunkt) |
| `sensor.druck_konfigurator_job` | Name des Druckauftrags |
| `sensor.druck_konfigurator_layer` | Schicht, z. B. `12/200` |
| `sensor.druck_konfigurator_nozzle_temp` / `_bed_temp` | Düse / Druckbett (°C) |
| `sensor.druck_konfigurator_queue_state` | Warteschlange als Text, z. B. „Platte 2 fertig – Bett abräumen, danach Platte 3“ |
| `sensor.druck_konfigurator_queue_remaining_min` | Restliche Druckzeit der Warteschlange (min, ohne Pausen zum Abräumen) |
| `sensor.druck_konfigurator_plates` | Platten fertig/gesamt, z. B. `2/5` (übersprungene zählen nicht) |
| `binary_sensor.druck_konfigurator_bed_clear` | **Bett abräumen**: an, sobald eine Platte der Warteschlange fertig ist; aus, wenn die nächste startet oder die Warteschlange endet |
| `sensor.druck_konfigurator_slot1_remaining` … | Restmenge je ACE-Slot (g) aus der Filamentverwaltung; Attribute `name`, `type`, `colour`, `net_g`, `brand` |
| `camera.druck_konfigurator_progress` | **3D-Fortschritt**: Bild des laufenden Drucks (schräg von oben, in den Farben der ACE-Slots), neu bei jeder Schicht – nur für Drucke aus dem Tool; ohne Anmeldung am Add-on nutzbar (Dashboard, Handy-App, Bild in Benachrichtigungen) |

Die Entitäts-IDs gelten ab Home Assistant 2025.10 (`default_entity_id`); ältere Versionen bilden sie aus dem Gerätenamen –
dann unter **Einstellungen → Geräte** nachsehen.

MQTT-Themen: `druck_konfigurator/state` (JSON, alle 15 s und bei Änderung), `druck_konfigurator/slot/<n>`, `druck_konfigurator/progress_image` (PNG),
`druck_konfigurator/availability` (`online`/`offline`, Last Will), Discovery unter `homeassistant/…/druck_konfigurator/…/config`.

Beispiel: Benachrichtigung aufs Handy, wenn das Bett abgeräumt werden muss
(`notify.mobile_app_mein_handy` durch den Dienst deiner Companion-App ersetzen):

```yaml
alias: "3D-Druck: Bett abräumen"
triggers:
  - trigger: state
    entity_id: binary_sensor.druck_konfigurator_bed_clear
    to: "on"
actions:
  - action: notify.mobile_app_mein_handy
    data:
      title: "Druck fertig – Bett abräumen"
      message: >-
        {{ states('sensor.druck_konfigurator_queue_state') }}
        ({{ states('sensor.druck_konfigurator_plates') }} Platten fertig)
      data:
        tag: druck-queue
        image: /api/camera_proxy/camera.druck_konfigurator_progress   # Bild des Drucks
mode: single
```

## Hinweise

- Architekturen: amd64 und aarch64 (z. B. Raspberry Pi 4/5). Das Image ist wegen OrcaSlicer rund 1,5 GB groß.
- Der Drucker muss aus Home Assistant erreichbar sein (gleiches Netz, private IP-Adresse).
- **Haftungsausschluss:** Nutzung auf eigene Verantwortung, ohne Gewährleistung. Das Tool kann den Drucker steuern und
  Drucke starten – Bett, Druckplatte und Filament prüfst du vor jedem Start selbst. Werte, Kosten und Restmengen sind
  Startwerte bzw. Schätzungen. Den optionalen Port 8765 nicht ins Internet freigeben (ohne `access_pin` hat er keine Anmeldung, und auch mit PIN läuft er unverschlüsselt über HTTP).
  Vollständig: [Haftungsausschluss im Projekt](https://github.com/TMA84/druck-konfigurator#haftungsausschluss).
- Lizenz: [CC BY-NC 4.0](https://github.com/TMA84/druck-konfigurator/blob/main/LICENSE) (nicht kommerziell);
  OrcaSlicer (AGPL-3.0) wird unverändert mitgeliefert.

## Dank

Der Druck-Konfigurator basiert auf dem **[Druck-Konfigurator von wolfb63-del](https://github.com/wolfb63-del/druck-konfigurator)** –
Empfehlungslogik, Datenblatt, 3D-Ansicht und 3MF-Export stammen von dort. Vielen Dank!
