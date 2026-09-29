# Changelog

## 10.4.0

- Druckkopf folgt den G-Code-Bahnen (echte Position, standardmäßig an), fährt flüssig zwischen den Meldungen
- Bahnen färben sich ein, sobald der Kopf sie abgefahren hat; Fortschritt innerhalb der Schicht in %

## 10.3.0

- Druckkopf im 3D-Fortschritt: geschätzt oder echte Position vom Drucker (Schalter „Echte Kopfposition“)
- Kommende Schichten durchsichtig, ausgeblendet oder voll

## 10.2.0

- **Mehrere ACE-Einheiten:** Kobra S1 bis 2 ACE (8 Slots), andere Anycubic-Drucker bis 4; Slots zählen durch (ACE 2 = Slot 5–8), Sensoren je Slot über alle Einheiten
- Einzelne Teile aus dem Projekt entfernen (mit Rückgängig)
- Licht/Trocknen: kein „nicht bestätigt“ mehr, wenn der Drucker den Befehl ausführt

## 10.1.0

- **PIN-Schutz** für den direkten Port 8765 (Option `access_pin`); die Seitenleiste bleibt durch Home Assistant geschützt
- Beschriftung: Text erhaben (eigene Farbe) oder vertieft auf Teile
- Druckhistorie & Statistik, Sensoren „Filament/Kosten/Drucke diesen Monat“
- Filamentprofil aus einer Spule, Tablet-Ansicht, schneller bei vielen Teilen

## 10.0.0

- **Home Assistant:** Sensoren über MQTT (Fortschritt, Restzeit, Warteschlange, „Bett abräumen“, Restmenge je Slot) – automatisch, wenn das Mosquitto-Add-on läuft (Option `mqtt_enabled`)
- Warteschlange auf dem Server: „Platte fertig“ auch ohne offene Seite
- 3D-Fortschritt im Tab Drucker
- Spulen: Export/Import, Gewicht bei neuer Spule abfragen, Warnschwelle
- Makerworld-Farben bleiben beim Kombinieren, Anordnen und bei Kopien erhalten

## 9.5.1

- Slot für alle Teile übernehmen (② und ③)

## 9.5.0

- Teile platzsparend anordnen: passen mehrere Teile auf eine Platte, landen sie auch dort (dreht bei Bedarf um 90°); auch für Makerworld-Projekte

## 9.4.0

- Modell hinzufügen: verschiedene Modelle kombiniert und mehrfach drucken
- Slot wählen auch bei einem einfarbigen Teil (③ Filament-Slots anklicken)

## 9.3.3

- Stützen: „Nur kritische Bereiche“ je Auftrag einstellbar (Werte anpassen) – aus = auch normale Überhänge werden gestützt

## 9.3.2

- Kamera: Fehler „Kamera nicht verfügbar (Exception)“ behoben (falsche Adresse hinter Ingress)

## 9.3.1

- Haftungsausschluss überarbeitet, Dank an das Ursprungsprojekt (wolfb63-del/druck-konfigurator)

## 9.3.0

- Fertiges Image aus GHCR (amd64/aarch64) – Home Assistant muss nichts mehr selbst bauen
- Option **printer_ip**: Drucker direkt in den Add-on-Einstellungen eintragen; die Seite verbindet sich von selbst,
  die Filamentverwaltung zählt ab dem Start mit

## 9.2.0

- Erste Version als Home-Assistant-Add-on (Ingress in der Seitenleiste, optional Port 8765)
- Druckwerte und 3MF für OrcaSlicer, Kosten mit exaktem Slicen, Slice-Vorschau
- Mehrere Platten mit Warteschlange, Farben des Designers → Slot
- Drucker-Werkbank für den Kobra S1 (Werksfirmware, LAN-Modus)
- Filamentverwaltung: Spulen erkennen, Restmenge errechnen
- Deutsch/Englisch, Hell/Dunkel
