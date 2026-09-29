# Changelog

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
