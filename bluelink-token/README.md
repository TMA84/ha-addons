# Bluelink Token Generator Add-on

Generiert Hyundai/Kia Bluelink Refresh Tokens für die Verwendung mit evcc und Home Assistant.

## Funktionsweise

1. Öffne die Web-UI des Addons (Port 9876)
2. Klicke auf "Login starten"
3. Du wirst zur Bluelink-Anmeldeseite weitergeleitet - melde dich an
4. Nach dem Login wirst du auf eine Seite weitergeleitet (evtl. mit Fehlermeldung - das ist normal!)
5. Kopiere die komplette URL aus der Adressleiste
6. Füge sie in das Eingabefeld ein und klicke auf "Token generieren"
7. Dein Refresh Token wird angezeigt

Kein Selenium oder Chrome nötig - alles läuft direkt in deinem Browser.

## Konfiguration

- **brand**: Fahrzeugmarke - `hyundai` oder `kia`

## Verwendung des Tokens

Verwende den Refresh Token als Passwort zusammen mit deinem normalen Benutzernamen bei der Einrichtung der evcc oder Home Assistant Integration.

Der Refresh Token ist **180 Tage** gültig. Danach muss ein neuer generiert werden.

## Credits

Basiert auf [bluelink_refresh_token](https://github.com/RustyDust/bluelink_refresh_token) von RustyDust.
