#!/usr/bin/env python3
"""
Bluelink Token Generator - Web Application
Handles the OAuth2 flow for Hyundai/Kia Bluelink in the user's browser.
No Selenium needed - the user logs in directly.
"""

import os
import requests
from flask import Flask, render_template_string, request, redirect, session
from urllib.parse import urlencode, urlparse, parse_qs

app = Flask(__name__)
app.secret_key = os.urandom(24)

BRAND_CONFIG = {
    "kia": {
        "client_id": "fdc85c00-0a2f-4c64-bcb4-2cfb1500730a",
        "client_secret": "secret",
        "base_url": "https://idpconnect-eu.kia.com/auth/api/v2/user/oauth2",
        "redirect_url_final": "https://prd.eu-ccapi.kia.com:8080/api/v1/user/oauth2/redirect",
        "login_params": {
            "ui_locales": "de",
            "scope": "openid profile email phone",
            "response_type": "code",
            "client_id": "peukiaidm-online-sales",
            "redirect_uri": "https://www.kia.com/api/bin/oneid/login",
            "state": "default",
        },
    },
    "hyundai": {
        "client_id": "6d477c38-3ca4-4cf3-9557-2a1929a94654",
        "client_secret": "KUy49XxPzLpLuoK0xhBC77W6VXhmtQR9iQhmIFjjoY4IpxsV",
        "base_url": "https://idpconnect-eu.hyundai.com/auth/api/v2/user/oauth2",
        "redirect_url_final": "https://prd.eu-ccapi.hyundai.com:8080/api/v1/user/oauth2/token",
        "login_params": {
            "client_id": "peuhyundaiidm-ctb",
            "redirect_uri": "https://ctbapi.hyundai-europe.com/api/auth",
            "nonce": "",
            "state": "NL_",
            "scope": "openid profile email phone",
            "response_type": "code",
            "connector_client_id": "peuhyundaiidm-ctb",
            "connector_scope": "",
            "connector_session_key": "",
            "country": "",
            "captcha": "1",
            "ui_locales": "en-US",
        },
    },
}

TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <title>Bluelink Token Generator</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
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
        .step { display: flex; gap: 12px; margin-bottom: 16px; }
        .step-num { width: 28px; height: 28px; border-radius: 50%; background: #e8e8e8;
                    display: flex; align-items: center; justify-content: center;
                    font-weight: 700; font-size: 14px; flex-shrink: 0; }
        .step-num.active { background: #4CAF50; color: white; }
        .step-text { padding-top: 3px; }
        .btn { display: inline-block; padding: 12px 28px; border-radius: 8px; border: none;
               color: white; font-size: 15px; font-weight: 600; cursor: pointer;
               text-decoration: none; transition: background 0.2s; }
        .btn-primary { background: #4CAF50; }
        .btn-primary:hover { background: #43a047; }
        .btn-blue { background: #1976D2; }
        .btn-blue:hover { background: #1565C0; }
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
        label { display: block; font-size: 14px; font-weight: 500; margin-bottom: 4px; }
    </style>
</head>
<body>
<div class="container">
    <h1>🔑 Bluelink Token Generator</h1>
    <p class="subtitle">Refresh Token für evcc & Home Assistant</p>

    {% block content %}{% endblock %}
</div>
<script>
function copyToken(id) {
    const text = document.getElementById(id).innerText;
    navigator.clipboard.writeText(text).then(() => {
        const btn = document.querySelector('[data-copy="' + id + '"]');
        btn.textContent = '✅ Kopiert!';
        setTimeout(() => btn.textContent = '📋 Kopieren', 2000);
    });
}
</script>
</body>
</html>
"""

PAGE_HOME = """
{% extends "base" %}
{% block content %}
<div class="card">
    <span class="brand-badge {{ brand }}">{{ brand|upper }}</span>

    <div class="step">
        <div class="step-num active">1</div>
        <div class="step-text">Klicke auf <strong>Login starten</strong> um zur Bluelink-Anmeldeseite weitergeleitet zu werden.</div>
    </div>
    <div class="step">
        <div class="step-num">2</div>
        <div class="step-text">Melde dich mit deinen Bluelink-Zugangsdaten an (die gleichen wie in der App).</div>
    </div>
    <div class="step">
        <div class="step-num">3</div>
        <div class="step-text">Nach dem Login wirst du zurückgeleitet und der Token wird automatisch generiert.</div>
    </div>

    <hr class="divider">

    <div class="actions">
        <a href="/login" class="btn btn-primary">🚀 Login starten</a>
    </div>
</div>

<div class="card">
    <div class="alert alert-info">
        💡 Du kannst die Marke in der Addon-Konfiguration ändern (hyundai/kia).
    </div>
</div>
{% endblock %}
"""

PAGE_CALLBACK = """
{% extends "base" %}
{% block content %}
<div class="card">
    <span class="brand-badge {{ brand }}">{{ brand|upper }}</span>

    <div class="alert alert-warning">
        ⏳ Nach dem Login bei {{ brand|title }} wirst du auf eine Seite weitergeleitet, die möglicherweise einen Fehler zeigt. Das ist normal!
    </div>

    <label for="redirect_url">Kopiere die komplette URL aus der Adressleiste deines Browsers hierher:</label>
    <form method="POST" action="/exchange">
        <input type="text" name="redirect_url" id="redirect_url"
               placeholder="https://prd.eu-ccapi.{{ brand }}.com:8080/..." autofocus>
        <div class="actions">
            <button type="submit" class="btn btn-blue">🔑 Token generieren</button>
            <a href="/" class="btn btn-outline">← Zurück</a>
        </div>
    </form>
</div>

<div class="card">
    <h3 style="margin-bottom: 8px;">Anleitung</h3>
    <ol style="padding-left: 20px; line-height: 1.8; font-size: 14px;">
        <li>Klicke auf den Button unten um dich bei {{ brand|title }} anzumelden</li>
        <li>Melde dich mit deinen Bluelink-Zugangsdaten an</li>
        <li>Du wirst auf eine Seite weitergeleitet (evtl. mit Fehlermeldung)</li>
        <li>Kopiere die <strong>komplette URL</strong> aus der Adressleiste</li>
        <li>Füge sie oben ein und klicke auf "Token generieren"</li>
    </ol>
    <hr class="divider">
    <a href="{{ login_url }}" target="_blank" class="btn btn-primary">🔗 Bei {{ brand|title }} anmelden</a>
</div>
{% endblock %}
"""

PAGE_SUCCESS = """
{% extends "base" %}
{% block content %}
<div class="card">
    <span class="brand-badge {{ brand }}">{{ brand|upper }}</span>
    <div class="alert alert-success">✅ Token erfolgreich generiert!</div>

    <div style="margin-bottom: 20px;">
        <div class="token-label">Refresh Token</div>
        <div class="token-box" id="refresh">{{ refresh_token }}</div>
        <button class="copy-btn" data-copy="refresh" onclick="copyToken('refresh')">📋 Kopieren</button>
    </div>

    <div style="margin-bottom: 20px;">
        <div class="token-label">Access Token</div>
        <div class="token-box" id="access">{{ access_token }}</div>
        <button class="copy-btn" data-copy="access" onclick="copyToken('access')">📋 Kopieren</button>
    </div>

    <div class="alert alert-warning">
        ⚠️ Der Refresh Token ist <strong>180 Tage</strong> gültig. Danach muss ein neuer generiert werden.
    </div>

    <hr class="divider">
    <p style="font-size: 14px; color: #666;">
        Verwende den <strong>Refresh Token</strong> als Passwort zusammen mit deinem
        normalen Benutzernamen bei der Einrichtung der evcc oder Home Assistant Integration.
    </p>
    <hr class="divider">
    <a href="/" class="btn btn-outline">🔄 Neuen Token generieren</a>
</div>
{% endblock %}
"""

PAGE_ERROR = """
{% extends "base" %}
{% block content %}
<div class="card">
    <span class="brand-badge {{ brand }}">{{ brand|upper }}</span>
    <div class="alert alert-error">❌ {{ error }}</div>
    <div class="actions">
        <a href="/" class="btn btn-primary">🔄 Erneut versuchen</a>
    </div>
</div>
{% endblock %}
"""


class TemplateRenderer:
    """Helper to render templates with base template inheritance."""
    def __init__(self):
        from jinja2 import BaseLoader, Environment
        self.env = Environment(loader=BaseLoader())

    def render(self, page_template, **kwargs):
        # Simple approach: replace block content
        full = TEMPLATE.replace("{% block content %}{% endblock %}", page_template)
        template = self.env.from_string(full)
        return template.render(**kwargs)


renderer = TemplateRenderer()


def get_brand():
    return os.environ.get("BRAND", "hyundai").lower()


@app.route("/")
def index():
    brand = get_brand()
    return renderer.render(PAGE_HOME, brand=brand)


@app.route("/login")
def login():
    brand = get_brand()
    config = BRAND_CONFIG[brand]

    # Build the login URL
    login_url = f"{config['base_url']}/authorize?" + urlencode(config["login_params"])

    # Build the redirect URL that will contain the auth code
    redirect_params = {
        "response_type": "code",
        "client_id": config["client_id"],
        "redirect_uri": config["redirect_url_final"],
        "lang": "de",
        "state": "ccsp",
    }
    auth_redirect_url = f"{config['base_url']}/authorize?" + urlencode(redirect_params)

    # Store for later use
    session["auth_redirect_url"] = auth_redirect_url

    return renderer.render(PAGE_CALLBACK, brand=brand, login_url=login_url)


@app.route("/exchange", methods=["POST"])
def exchange():
    brand = get_brand()
    config = BRAND_CONFIG[brand]
    redirect_url = request.form.get("redirect_url", "").strip()

    if not redirect_url:
        return renderer.render(PAGE_ERROR, brand=brand, error="Keine URL eingegeben.")

    # Extract code from URL
    try:
        parsed = urlparse(redirect_url)
        params = parse_qs(parsed.query)
        code = params.get("code", [None])[0]

        if not code:
            # Try to find code in fragment
            if parsed.fragment:
                frag_params = parse_qs(parsed.fragment)
                code = frag_params.get("code", [None])[0]

        if not code:
            return renderer.render(
                PAGE_ERROR, brand=brand,
                error=f"Kein Autorisierungscode in der URL gefunden. Bitte kopiere die komplette URL nach dem Login."
            )
    except Exception as e:
        return renderer.render(PAGE_ERROR, brand=brand, error=f"URL konnte nicht verarbeitet werden: {e}")

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
        response = requests.post(token_url, data=data, timeout=15)
        if response.status_code == 200:
            tokens = response.json()
            return renderer.render(
                PAGE_SUCCESS, brand=brand,
                refresh_token=tokens.get("refresh_token", "N/A"),
                access_token=tokens.get("access_token", "N/A"),
            )
        else:
            return renderer.render(
                PAGE_ERROR, brand=brand,
                error=f"API Fehler {response.status_code}: {response.text[:200]}"
            )
    except Exception as e:
        return renderer.render(PAGE_ERROR, brand=brand, error=f"Verbindungsfehler: {e}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9876)
