#!/usr/bin/env python3
"""
Bluelink Token Generator - Web Application
OAuth2 flow for Hyundai/Kia Bluelink.

The flow works like the original Selenium script but in the user's browser:
1. User logs in on the brand's login page
2. After login, user clicks the API authorize link (same browser session!)
3. The redirect URL contains the auth code
4. User pastes the URL back here to exchange for tokens
"""

import os
import re
import requests as req_lib
from flask import Flask, request
from urllib.parse import urlencode, urlparse, parse_qs
import html as html_lib

app = Flask(__name__)

BRAND_CONFIG = {
    "kia": {
        "client_id": "fdc85c00-0a2f-4c64-bcb4-2cfb1500730a",
        "client_secret": "secret",
        "base_url": "https://idpconnect-eu.kia.com/auth/api/v2/user/oauth2",
        "redirect_url_final": "https://prd.eu-ccapi.kia.com:8080/api/v1/user/oauth2/redirect",
        "login_url": "https://idpconnect-eu.kia.com/auth/api/v2/user/oauth2/authorize?ui_locales=de&scope=openid%20profile%20email%20phone&response_type=code&client_id=peukiaidm-online-sales&redirect_uri=https%3A%2F%2Fwww.kia.com%2Fapi%2Fbin%2Foneid%2Flogin&state=aHR0cHM6Ly93d3cua2lhLmNvbTo0NDMvZGUvP21zb2NraWQ9MjM1NDU0ODBmNmUyNjg5NDIwMmU0MDBjZjc2OTY5NWQmX3RtPTE3NTYzMTg3MjY1OTImX3RtPTE3NTYzMjQyMTcxMjY%3D_default",
        "code_pattern": r'^https://.*:8080/api/v1/user/oauth2/redirect',
    },
    "hyundai": {
        "client_id": "6d477c38-3ca4-4cf3-9557-2a1929a94654",
        "client_secret": "KUy49XxPzLpLuoK0xhBC77W6VXhmtQR9iQhmIFjjoY4IpxsV",
        "base_url": "https://idpconnect-eu.hyundai.com/auth/api/v2/user/oauth2",
        "redirect_url_final": "https://prd.eu-ccapi.hyundai.com:8080/api/v1/user/oauth2/token",
        "login_url": "https://idpconnect-eu.hyundai.com/auth/api/v2/user/oauth2/authorize?client_id=peuhyundaiidm-ctb&redirect_uri=https%3A%2F%2Fctbapi.hyundai-europe.com%2Fapi%2Fauth&nonce=&state=NL_&scope=openid+profile+email+phone&response_type=code&connector_client_id=peuhyundaiidm-ctb&connector_scope=&connector_session_key=&country=&captcha=1&ui_locales=en-US",
        "code_pattern": r'^https://.*:8080/api/v1/user/oauth2/token',
    },
}

STYLE = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
       background: #f0f2f5; color: #333; min-height: 100vh; padding: 20px; }
.container { max-width: 640px; margin: 0 auto; }
h1 { font-size: 24px; margin-bottom: 8px; }
.subtitle { color: #666; margin-bottom: 24px; }
.card { background: white; border-radius: 12px; padding: 24px;
        margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.brand-badge { display: inline-block; padding: 4px 14px; border-radius: 20px;
               font-weight: 600; font-size: 13px; color: white; margin-bottom: 16px; }
.brand-badge.hyundai { background: #002C5F; }
.brand-badge.kia { background: #05141F; }
.step { display: flex; gap: 12px; margin-bottom: 16px; align-items: flex-start; }
.step-num { width: 28px; height: 28px; border-radius: 50%; background: #e8e8e8;
            display: flex; align-items: center; justify-content: center;
            font-weight: 700; font-size: 14px; flex-shrink: 0; }
.step-num.done { background: #4CAF50; color: white; }
.step-num.active { background: #1976D2; color: white; }
.step-text { padding-top: 3px; line-height: 1.5; }
.btn { display: inline-block; padding: 12px 28px; border-radius: 8px; border: none;
       color: white; font-size: 15px; font-weight: 600; cursor: pointer;
       text-decoration: none; transition: background 0.2s; margin-top: 8px; }
.btn-primary { background: #4CAF50; }
.btn-primary:hover { background: #43a047; }
.btn-blue { background: #1976D2; }
.btn-blue:hover { background: #1565C0; }
.btn-orange { background: #F57C00; }
.btn-orange:hover { background: #EF6C00; }
.btn-outline { background: transparent; color: #666; border: 1px solid #ddd; }
.btn-outline:hover { background: #f5f5f5; }
.token-label { font-size: 13px; font-weight: 600; color: #666;
               text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }
.token-box { background: #f8f9fa; border: 1px solid #e0e0e0; padding: 12px 14px;
             border-radius: 8px; word-break: break-all; font-family: 'SF Mono', monospace;
             font-size: 13px; margin-bottom: 6px; line-height: 1.5; }
.copy-btn { background: none; border: none; color: #1976D2; cursor: pointer;
            font-size: 13px; padding: 4px 0; }
.copy-btn:hover { text-decoration: underline; }
.url-box { background: #f0f0f0; padding: 10px 14px; border-radius: 8px;
           word-break: break-all; font-family: monospace; font-size: 12px;
           margin: 8px 0; border: 1px solid #ddd; user-select: all; }
.alert { padding: 12px 16px; border-radius: 8px; margin-bottom: 16px; font-size: 14px; }
.alert-success { background: #e8f5e9; color: #2e7d32; }
.alert-error { background: #fbe9e7; color: #c62828; }
.alert-warning { background: #fff8e1; color: #f57f17; }
.alert-info { background: #e3f2fd; color: #1565c0; }
.divider { border: none; border-top: 1px solid #eee; margin: 20px 0; }
.actions { display: flex; gap: 10px; flex-wrap: wrap; }
input[type="text"] { width: 100%; padding: 10px 14px; border: 1px solid #ddd;
                     border-radius: 8px; font-size: 15px; margin-bottom: 12px; }
input[type="text"]:focus { outline: none; border-color: #1976D2; }
label { display: block; font-size: 14px; font-weight: 500; margin-bottom: 6px; }
code { background: #f0f0f0; padding: 2px 6px; border-radius: 4px; font-size: 13px; }
"""

COPY_SCRIPT = """
function copyToken(id) {
    var text = document.getElementById(id).innerText;
    navigator.clipboard.writeText(text).then(function() {
        var btn = document.querySelector('[data-copy="' + id + '"]');
        btn.textContent = '✅ Kopiert!';
        setTimeout(function() { btn.textContent = '📋 Kopieren'; }, 2000);
    });
}
"""


def render(content):
    return f"""<!DOCTYPE html>
<html lang="de"><head>
<title>Bluelink Token Generator</title>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<style>{STYLE}</style></head><body>
<div class="container">
<h1>🔑 Bluelink Token Generator</h1>
<p class="subtitle">Refresh Token für evcc &amp; Home Assistant</p>
{content}
</div><script>{COPY_SCRIPT}</script></body></html>"""


def get_brand():
    return os.environ.get("BRAND", "hyundai").lower()


def get_code_url(brand):
    config = BRAND_CONFIG[brand]
    return (f"{config['base_url']}/authorize?"
            f"response_type=code&"
            f"client_id={config['client_id']}&"
            f"redirect_uri={config['redirect_url_final']}&"
            f"lang=de&state=ccsp")


def extract_code(url_str):
    """Extract auth code from redirect URL."""
    # Try query parameter first
    parsed = urlparse(url_str)
    params = parse_qs(parsed.query)
    code = params.get("code", [None])[0]
    if code:
        return code
    # Try regex pattern (code format: uuid.uuid.uuid)
    match = re.search(r'code=([0-9a-fA-F-]{36}\.[0-9a-fA-F-]{36}\.[0-9a-fA-F-]{36})', url_str)
    if match:
        return match.group(1)
    return None


@app.route("/")
def index():
    brand = get_brand()
    bt = brand.title()
    config = BRAND_CONFIG[brand]
    login_url = config["login_url"]
    code_url = get_code_url(brand)

    return render(f"""
<div class="card">
    <span class="brand-badge {brand}">{brand.upper()}</span>

    <div class="step">
        <div class="step-num active">1</div>
        <div class="step-text">
            Öffne den Login-Link und melde dich mit deinen {bt} Bluelink-Zugangsdaten an
            (die gleichen wie in der App).<br>
            <a href="{login_url}" target="_blank" class="btn btn-blue" style="margin-top:12px">
                🔗 Bei {bt} anmelden
            </a>
        </div>
    </div>

    <div class="step">
        <div class="step-num active">2</div>
        <div class="step-text">
            <strong>Wichtig: Im gleichen Browser!</strong> Öffne nach dem Login diesen Link.
            Du wirst auf eine Seite weitergeleitet die einen Fehler zeigt oder nicht lädt.
            <strong>Das ist normal!</strong><br>
            <a href="{code_url}" target="_blank" class="btn btn-orange" style="margin-top:12px">
                🔗 API-Autorisierung öffnen
            </a>
        </div>
    </div>

    <div class="step">
        <div class="step-num active">3</div>
        <div class="step-text">
            Kopiere die <strong>komplette URL</strong> aus der Adressleiste des Browsers
            (die Seite die den Fehler zeigt) und füge sie unten ein.
            Die URL enthält <code>?code=</code> - das ist der Auth-Code.
        </div>
    </div>

    <hr class="divider">

    <label for="redirect_url">URL aus Schritt 2 hier einfügen:</label>
    <form method="POST" action="/exchange">
        <input type="text" name="redirect_url" id="redirect_url"
               placeholder="https://prd.eu-ccapi.{brand}.com:8080/...?code=..." autofocus>
        <div class="actions">
            <button type="submit" class="btn btn-primary">🔑 Token generieren</button>
        </div>
    </form>
</div>

<div class="card">
    <div class="alert alert-info">
        💡 Marke ändern: Addon-Konfiguration → brand → hyundai oder kia
    </div>
    <div class="alert alert-warning">
        ⚠️ Schritt 1 und 2 müssen im <strong>gleichen Browser</strong> durchgeführt werden,
        damit die Login-Session erhalten bleibt!
    </div>
</div>""")


@app.route("/exchange", methods=["POST"])
def exchange():
    brand = get_brand()
    config = BRAND_CONFIG[brand]
    redirect_url = request.form.get("redirect_url", "").strip()

    if not redirect_url:
        return render(f"""
<div class="card">
    <span class="brand-badge {brand}">{brand.upper()}</span>
    <div class="alert alert-error">❌ Keine URL eingegeben.</div>
    <a href="/" class="btn btn-primary">← Zurück</a>
</div>""")

    code = extract_code(redirect_url)
    if not code:
        return render(f"""
<div class="card">
    <span class="brand-badge {brand}">{brand.upper()}</span>
    <div class="alert alert-error">❌ Kein Autorisierungscode in der URL gefunden.</div>
    <p style="margin: 12px 0; font-size: 14px;">
        Die URL muss <code>?code=</code> enthalten. Stelle sicher, dass du:
    </p>
    <ol style="padding-left: 20px; line-height: 1.8; font-size: 14px;">
        <li>Dich zuerst bei {brand.title()} angemeldet hast (Schritt 1)</li>
        <li>Dann im <strong>gleichen Browser</strong> den API-Link geöffnet hast (Schritt 2)</li>
        <li>Die <strong>komplette URL</strong> aus der Adressleiste kopiert hast</li>
    </ol>
    <a href="/" class="btn btn-primary" style="margin-top: 12px;">← Zurück</a>
</div>""")

    # Exchange code for tokens
    token_url = f"{config['base_url']}/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config["redirect_url_final"],
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
    }

    try:
        response = req_lib.post(token_url, data=data, timeout=15)
        if response.status_code == 200:
            tokens = response.json()
            rt = html_lib.escape(tokens.get("refresh_token", "N/A"))
            at = html_lib.escape(tokens.get("access_token", "N/A"))
            return render(f"""
<div class="card">
    <span class="brand-badge {brand}">{brand.upper()}</span>
    <div class="alert alert-success">✅ Token erfolgreich generiert!</div>
    <div style="margin-bottom: 20px;">
        <div class="token-label">Refresh Token</div>
        <div class="token-box" id="refresh">{rt}</div>
        <button class="copy-btn" data-copy="refresh" onclick="copyToken('refresh')">📋 Kopieren</button>
    </div>
    <div style="margin-bottom: 20px;">
        <div class="token-label">Access Token</div>
        <div class="token-box" id="access">{at}</div>
        <button class="copy-btn" data-copy="access" onclick="copyToken('access')">📋 Kopieren</button>
    </div>
    <div class="alert alert-warning">
        ⚠️ Der Refresh Token ist <strong>180 Tage</strong> gültig.
    </div>
    <hr class="divider">
    <p style="font-size: 14px; color: #666;">
        Verwende den <strong>Refresh Token</strong> als Passwort zusammen mit deinem
        normalen Benutzernamen bei der Einrichtung der evcc oder Home Assistant Integration.
    </p>
    <hr class="divider">
    <a href="/" class="btn btn-outline">🔄 Neuen Token generieren</a>
</div>""")
        else:
            err = html_lib.escape(response.text[:300])
            return render(f"""
<div class="card">
    <span class="brand-badge {brand}">{brand.upper()}</span>
    <div class="alert alert-error">❌ API Fehler {response.status_code}: {err}</div>
    <a href="/" class="btn btn-primary">← Zurück</a>
</div>""")
    except Exception as e:
        return render(f"""
<div class="card">
    <span class="brand-badge {brand}">{brand.upper()}</span>
    <div class="alert alert-error">❌ Verbindungsfehler: {html_lib.escape(str(e))}</div>
    <a href="/" class="btn btn-primary">← Zurück</a>
</div>""")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9876)
