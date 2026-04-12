# Bluelink Token Generator Add-on

Generiert Hyundai/Kia Bluelink Refresh Tokens für die Verwendung mit evcc und Home Assistant.

## Funktionsweise

Das Addon startet einen Chromium-Browser im Hintergrund mit dem korrekten Mobile User-Agent. Über noVNC kannst du den Browser direkt in deinem Webbrowser sehen und dich anmelden.

1. Öffne die Web-UI des Addons (Port 9876)
2. Klicke auf "Token-Generierung starten"
3. Im noVNC-Fenster siehst du den Chromium-Browser mit der Login-Seite
4. Melde dich mit deinen Bluelink-Zugangsdaten an
5. Das Script erkennt den erfolgreichen Login automatisch und generiert den Token

## Ports

- **9876**: Web-UI (Steuerung und Token-Anzeige)
- **6080**: noVNC (Browser-Ansicht)

## Konfiguration

- **brand**: Fahrzeugmarke - `hyundai` oder `kia`

## Verwendung des Tokens

Verwende den Refresh Token als Passwort zusammen mit deinem normalen Benutzernamen bei der Einrichtung der evcc oder Home Assistant Integration.

Der Refresh Token ist **180 Tage** gültig. Danach muss ein neuer generiert werden.

## Credits

Basiert auf [bluelink_refresh_token](https://github.com/RustyDust/bluelink_refresh_token) von RustyDust.
