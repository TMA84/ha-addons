# Changelog

## 10.34.4

- 3D-Fortschritt: Schleppkette als waagerechter Bogen über links, Filamentschlauch hängt links an der Kette (vorher überschnitten sie sich)

## 10.34.2

- 3D-Fortschritt: Gehäuselüfter mit sichtbarem Rad und Gitter, Abluft als Kegel zum Lüfter und Strahl nach draußen

## 10.34.1

- 3D-Fortschritt: Abluft des Gehäuselüfters sichtbar durchs Gitter nach draußen

## 10.34.0

- 3D-Fortschritt: Lüfter mit Luftstrom und drehenden Rädern (Bauteillüfter am Kopf, Hotend-Lüfter, Seitenlüfter rechts mit flacher Düse, Gehäuselüfter hinten) nach den gemeldeten Werten; Stangen und Riemen nach Foto des Kobra S1

## 10.33.3

- 3D-Fortschritt: Druckkopf höher (Riemen enden im Kopf), orangener Ring von allen Seiten sichtbar, Filament bis zur Düsenspitze, Z-Spindeln am Druckbett mit Haltern

## 10.33.0

- 3D-Fortschritt: gedruckte Bahnen sofort in Filamentfarbe, Riemen laufen physikalisch richtig, Proportionen wie beim Kobra S1 (Gehäuse, Motoren, Stangen)

## 10.32.1

- 3D-Fortschritt: Motoren auf der Höhe ihres Riemens (rechts oben, links unten wie im Kobra S1)

## 10.32.0

- 3D-Fortschritt: laufende Riemen (CoreXY bzw. Bettschubser), Schleppkette und Filamentschlauch in der Farbe der aktuellen Bahn

## 10.31.1

- Höchstwerte ohne eigene Zeile: Tempo und Beschleunigung gehen nie über die Herstellerangabe; eine höhere Eingabe wird darauf gesetzt, das Feld sagt es

## 10.31.0

- Anordnen: Abstand zählt ab dem Brim, Berechnung im Hintergrund (Seite bleibt bedienbar), schräg in 45°-Schritten, wenn es eine Platte spart
- Warteschlange: Hinweis, wenn das Projekt jetzt weniger Platten braucht, mit „Warteschlange neu anlegen“
- Eingabefehler am Formular statt Browser-Popup; eigenes Hotend-Maximum (Volumenstrom) je Drucker

## 10.30.0

- Höchstwerte je Drucker: Geschwindigkeit und Beschleunigung aus dem Orca-Profil (Kobra S1 600 mm/s, 20 000 mm/s²) werden nie überschritten – auch nicht durch Anpassungen; eigene Höchstwerte im Reiter Tempo

## 10.29.0

- Anordnen nach echter Grundfläche: Rahmen, Winkel und Dreiecke werden ineinander gelegt (auch 180° gedreht) statt je eine eigene Platte – z. B. 5 statt 9 Platten; Draufsicht zeigt die Umrisse

## 10.28.0

- Weitere Anycubic mit LAN-Modus (experimentell): Kobra S1 Max, Kobra 3 / Combo / Max, Kobra X – Drucken, Werkbank, ACE, Warteschlange; 3D-Fortschritt je Bauart (CoreXY oder Bettschubser); Senden sperrt bei falschem Modell
- Behoben: „Slice-Auftrag nicht (mehr) vorhanden“ nach Add-on-Neustart – Aufträge liegen jetzt in /data, fehlt einer, wird neu geslict

## 10.27.3

- Warteschlange wird sofort angelegt (Platten im Hintergrund gesichert), mit Rückmeldung am Knopf
- „Änderungen für alle Teile“ standardmäßig an
- Behoben: weitere Orca-Einstellungen (z. B. Stützen-Typ) wirkten nicht im Objekt
- Stützen: „Stützen bis Neigung (zur Waagerechten)“ verständlich beschriftet, neu „Kleine Überhänge weglassen“
- 3D-Fortschritt: Druckkopf leicht durchsichtig

## 10.27.2

- Behoben: schräge Überhänge über dem Grenzwinkel bekamen keine Stützen – „Nur kritische Bereiche“ ist als Vorschlag jetzt aus

## 10.27.1

- 3D-Fortschritt: Stangen silbern, die zwei X-Stangen übereinander, drei Z-Spindeln (hinten Mitte, vorne links/rechts) – wie am Kobra S1

## 10.27.0

- 3D-Fortschritt als Nachbildung des Kobra S1: weißer Kopf mit orangem Streifen, Kupferstangen, blaue Motoren, Rahmen mit Z-Spindeln, PEI-Platte

## 10.26.0

- Neuer Name: Druckwerkstatt (Seitenleiste und Add-on-Name; Kennung, Daten und MQTT-Entitäten bleiben)
- 3D-Fortschritt: Schienen und Laufwagen richtig verbunden, Petrol-Streifen am Druckkopf entfernt
- Handbuch, README und Bilder aktualisiert

## 10.25.0

- Druckwerte als Werte-Tafel: Reiter + Tabelle Einstellung | Wert | Vorschlag, direkt bearbeitbar (Dialog entfällt)
- 3D-Fortschritt: Druckkopf und Schienen neu gestaltet
- Knopf „Neue Spule eingelegt“ für eine neue Spule gleicher Sorte und Farbe
- Fortschrittsbalken in Petrol statt Orange

## 10.24.0

- 3D-Fortschritt als beleuchtete Raupen mit Druckplatte, Hintergrund passend zu hell/dunkel
- Links „Verbindung …“ und „Rohdaten“ in Petrol statt Orange

## 10.23.0

- Druckwerte ruhiger: Kennzahlen oben, darunter je Thema eine Liste „Bezeichnung … Wert“
- Abschnitt „Einstellungen in OrcaSlicer-Reihenfolge“ entfernt
- Behoben: Warteschlange – nächste Platte ließ sich nicht starten (Slice-Auftrag wird jetzt dauerhaft aufgehoben)

## 10.22.0

- Neues Farbschema Graphit + Petrol (hell und dunkel)
- Druckwerte: alle Werte als Kacheln nach Thema, nichts eingeklappt
- Werte anpassen: Reiter nach Thema mit Zähler und Suche über alle Reiter

## 10.21.0

- Form innen für den Brim: nur große Löcher, alle Löcher mit freier Mitte, nur Lochecken, Orca innen ringsum

## 10.20.0

- Brim-Abschnitt: außen und innen getrennt an/aus, Form außen, Abstand zum Teil
- Zeile „In Orca“ zeigt, welche Orca-Einstellungen für das Teil geschrieben werden

## 10.19.1

- Behoben: Brim fehlte an langen geraden Kanten und neben Schlitzen – dichte Ohrenkette entlang des Umrisses, kleinere Ohren neben Löchern

## 10.19.0

- Brim innen als eigene Auswahl (aus / 2 / 3 / 5 mm): nur große Löcher, kleine Löcher und Schriften bleiben frei; auch ohne äußeren Brim

## 10.18.2

- Behoben: je nach Teilhöhe kein Brim (nur mit Raft) – Mausohren lagen durch Rundung minimal über dem Bett

## 10.18.1

- Brim lässt Löcher und Schriften frei (gesetzte Mausohren am Außenumriss statt Rundum-Brim um Inseln)
- Innerer Brim nur noch in großen Löchern, eigene Brim-Breite innen
- Brim-Art nur noch einmal (direkt unter Brim)

## 10.18.0

- Druckwerte: neue Karte „Weitere Orca-Einstellungen“ (Stützen-Typ, Elefantenfuß, Wandgenerator, Bügeln, Brim-Art …), Kachel anklicken öffnet den Dialog
- Weniger doppelte Hinweise; Stützen-Typ „Normal“ wird korrekt benannt

## 10.17.0

- Rund 30 weitere Orca-Einstellungen je Auftrag: Stützen-Typ und -Stil, Elefantenfuß-Kompensation, Arachne, Bügeln, Brim-Art, Raft …
- Behoben: bei geplanten Drucken (z. B. mit Vorwärmen) fehlte der 3D-Fortschritt

## 10.16.0

- Angepasste Werte als Standard je Drucker und Filament merken – gespeichert im Add-on, gelten in jedem Browser
- Behoben: bei mehreren Teilen gingen angepasste Slot- und Plattenwerte (Temperaturen, Lüfter, erste Schicht …) am zweiten Teil verloren

## 10.15.0

- Alle Werte, die das Tool in den Druck schreibt, sind je Auftrag anpassbar – immer mit Vorschlag und Warnung bei starker Abweichung
- Behoben: bei ABS/ASA löste sich der Brim vom Teil (Brim jetzt ohne Spalt, am kompensierten Umriss)

## 10.14.0

- Kobra-S1-Vorgaben je Filament: Hilfs-/Gehäuselüfter, bei ABS/ASA Bett ≥ 100 °C, 5 mm Brim und 10 min Vorwärmen
- Werkbank: geplanter Druck als volle Zeile, Druckauftrag zeigt „Bett heizt vor – Druck startet um …“

## 10.13.0

- Bett vorwärmen vor dem Druck (sofort oder vor geplantem Start); Heizung aus bei Absage oder Fehlstart
- Hilfs- und Gehäuselüfter je Auftrag einstellbar (Kobra S1)
- Behoben: „Werte für diesen Auftrag“ rundete Kommastellen weg (z. B. Rückzug 1,3 → 1 mm)
- „Geplanter Druck“ in Home Assistant kennt den Zustand „heizt vor“

## 10.12.2

- Behoben: 3D-Fortschritt zeigte beim Bett vermessen das Modell als fertig

## 10.12.1

- Behoben: „An Drucker senden“ öffnete sich in 10.12.0 nicht

## 10.12.0

- Druck zeitlich planen (Sendedialog → „Später starten“), optional vorher trocknen; der Server startet zur Zeit nach erneuter Prüfung
- Neue Sensoren „Geplanter Start“ (`sensor.druck_konfigurator_schedule_start`) und „Geplanter Druck“ (`…_schedule_state`)
- Tempo und Rückzug je Auftrag einstellbar (erste Schicht, Travel, Beschleunigung, Rückzug)

## 10.11.2

- Behoben: Drucker zeigte das Modell nach dem Hochladen nicht an – das Tool setzt jetzt selbst ein Vorschaubild in den G-Code
- Behoben: 3MF aus Bambu Studio mit Objekten auf „nicht drucken“ ließ sich nicht slicen

## 10.11.1

- Jedes Objekt lässt sich überspringen, auch das letzte noch laufende (mit deutlicher Rückfrage)

## 10.11.0

- Seite lädt schneller: Dateien bleiben im Browser-Cache, gzip – erneutes Öffnen 5 KB statt 2,1 MB
- Neuer Sensor „Filament knapp“ (`binary_sensor.druck_konfigurator_filament_low`)
- Neue Option **Steuern aus Home Assistant** (`mqtt_control`, Standard aus): Knöpfe „Druck pausieren“ / „Druck fortsetzen“
- Druckzeiten mit Vorbereitung (Bett vermessen, Aufheizen)
- Weniger Rauschen im Add-on-Log (Routine-Abfragen nicht mehr protokolliert)

## 10.10.0

- Neue Kamera-Entität „3D-Fortschritt“ (`camera.druck_konfigurator_progress`): Bild des Drucks je Schicht – für Dashboard, Handy-App und Benachrichtigungen mit Bild
- Sätze zusammenhalten: jeder Satz eines Modells aus mehreren Teilen auf einer Platte
- Falsches Filament (Druckwerte ↔ Slot) wird schon vor dem Slicen gemeldet
- Restzeit rechnet Bettvermessung und Aufheizen mit; Druckhistorie endet bei „fertig“ statt erst beim nächsten Druck
- Behoben: Seite lud manchmal unvollständig („… is not defined“) – der Server wies Verbindungen ab
- Modell-Ansicht aufgeräumt

## 10.9.6

- Nur 3D-Fortschritt zum Einbetten: `/api/hassio_ingress/<Kennung>/?ansicht=3d` als Webseiten-Karte im Dashboard

## 10.9.5

- Behoben: Objektliste im Druck sprang beim Scrollen nach wenigen Sekunden zurück

## 10.9.4

- Objekte überspringen: Objekt im 3D-Fortschritt blau hervorheben, Rückfrage direkt in der Liste
- Behoben: nach einem Neustart des Druckers blieb er im Tool „busy“ – Verbindung baut sich jetzt neu auf, kein alter Stand mehr

## 10.9.3

- Werkbank: Z-Knöpfe als Bett ↑ / Bett ↓
- Senden: Hinweis, wenn der Drucker ohne Auftrag „beschäftigt“ meldet (Display prüfen), mit „Erneut abfragen“
- Senden: „Filament aus der ACE übernehmen und neu slicen“ bei falschem Material

## 10.9.2

- SUNLU-Farben mit den echten Farbcodes von sunlu.com, fehlende Farben ergänzt

## 10.9.1

- Umschalter „Farben | Grenzwinkel“ unter dem Modell (bleibt gemerkt)
- Grenzwinkel bei einfachen Teilen wieder sichtbar

## 10.9.0

- Anzahl für ein ganzes Modell (z. B. 20 Sätze RFID-Halter mit einer Eingabe), Kopien als eine Zeile
- Platten: Abstand zwischen Teilen einstellbar (3–15 mm), Teile als kompakter Block in der Mitte, Kopien je Platte als eine Zeile
- Modell und Druckwerte übersichtlicher: Werkzeuge als Reiter, Druckwerte in Gruppen, Spülmenge bei den Druckwerten
- Druck: eigene, ruhigere Restzeit; Objekte direkt in der 3D-Ansicht überspringen, übersprungene Bahnen dunkel
- STL in Zoll erkennen und umrechnen; Historie zeigt übersprungene Objekte

## 10.8.3

- Kamera startet von selbst, sobald sie im Tab ④ zu sehen ist; in der 3D-Ansicht läuft kein Kamerastrom im Hintergrund

## 10.8.2

- Kamerabild auch auf dem iPhone (ab iOS 17.1): neuer Player mpegts.js statt flv.js

## 10.8.1

- Druckwerte: Farben des Herstellers nur noch, wenn die ACE die Farbe nicht per RFID gelesen hat

## 10.8.0

- Objekte während des Drucks überspringen (Tab ④ → Druckauftrag → Objekte), z. B. wenn sich ein Teil gelöst hat – für Drucke aus dem Tool
- Kamera zeigte oft ein altes Bild: Bild kommt jetzt ohne Verzögerung durch, die Kamera verbindet sich bei Stillstand neu

## 10.7.1

- STL-Dateien in Meter (z. B. aus Blender oder Onshape) werden auf Millimeter umgerechnet – vorher waren sie winzig und ließen sich nicht slicen

## 10.7.0

- Bemalen wie in OrcaSlicer: Farbe, Stützen (erzwingen/verhindern) und Naht je Fläche – Kreis, Kugel, Dreieck, Füllen mit Vorschau, Höhenbereich, Lücken füllen, Radierer; auch auf Makerworld-Modellen
- Filamente von Anycubic und SUNLU mit den Druckwerten der Hersteller und ihren Farben; Farbe anklicken trägt sie für den Slot ein
- Rückgängig / Wiederholen (Strg/⌘+Z) für das ganze Projekt
- Beschriftung auch auf Objekten des Designers (Makerworld-3MF); gewählte Bohrlöcher bleiben bei Größe und Drehung erhalten
- Handbuch-Bilder erneuert

## 10.6.1

- Ladebalken beim Slicen im Tab ③ und Kreisel am Reiter, wenn im Hintergrund geslict wird

## 10.6.0

- Slot-Zuordnung wie in OrcaSlicer: Slot-Chips, „Modell → Slot“ für die Filamente des Designers, automatische Zuordnung nach Farbe und Material; Filament folgt dem Slot
- Bemalung je Dreieck und Farb-Modifikatoren von Makerworld-Modellen werden angezeigt und auf die eigenen Slots umgeschrieben
- Werkzeugleiste in der 3D-Ansicht, Größe ändern, Drehen/Trennen auch bei Makerworld-3MF, ganze Platte zeigen
- Druck Objekt für Objekt, Projekt übersteht Neuladen, Modell entfernen, aufgeräumte Druckwerte, Handy-Ansicht

## 10.5.0

- Druckkopf fährt mit den Geschwindigkeiten aus dem G-Code und einem Bewegungsplaner wie Klipper – am echten Druck auf ±5 % genau
- Mechanik im 3D-Fortschritt: Bett, X-Traverse, Y-Schienen; Kopf in etwa echter Größe
- Gedruckte Bahnen der aktuellen Schicht werden orange, noch nicht gedruckte bleiben blass

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
