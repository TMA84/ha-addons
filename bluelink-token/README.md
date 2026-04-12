# Bluelink Token Generator Add-on

Generiert Hyundai/Kia Bluelink Refresh Tokens für die Verwendung mit evcc und Home Assistant.

## Funktionsweise

Dieses Addon stellt eine Web-Oberfläche bereit, über die du den Bluelink Login-Prozess durchführen kannst. Es nutzt Selenium mit Chromium um den OAuth-Flow abzuwickeln.

1. Öffne die Web-UI des Addons (Port 9876)
2. Klicke auf "Token generieren"
3. Melde dich im Browser-Fenster mit deinen Bluelink-Zugangsdaten an
4. Der Refresh Token wird automatisch extrahiert und angezeigt

## Konfiguration

- **brand**: Fahrzeugmarke - `hyundai` oder `kia`

## Verwendung des Tokens

Verwende den Refresh Token als Passwort zusammen mit deinem normalen Benutzernamen bei der Einrichtung der Home Assistant oder evcc Integration.

Der Refresh Token ist 180 Tage gültig. Danach muss ein neuer generiert werden.

## Credits

Basiert auf [bluelink_refresh_token](https://github.com/RustyDust/bluelink_refresh_token) von RustyDust.
