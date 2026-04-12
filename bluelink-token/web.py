#!/usr/bin/env python3
"""
Web UI for Bluelink Token Generator.
Runs headless Chrome to get the OAuth login URL, then provides
a simple web interface for the user to complete the login flow.
"""

import os
import re
import json
import time
import threading
import requests as req_lib
from flask import Flask, render_template_string, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

app = Flask(__name__)

# Global state
state = {
    "status": "idle",
    "refresh_token": None,
    "access_token": None,
    "error": None,
}

BRAND_CONFIG = {
    "kia": {
        "client_id": "fdc85c00-0a2f-4c64-bcb4-2cfb1500730a",
        "client_secret": "secret",
        "redirect_url_final": "https://prd.eu-ccapi.kia.com:8080/api/v1/user/oauth2/redirect",
        "success_selector": "a[class='logout user']",
        "login_url": "https://idpconnect-eu.kia.com/auth/api/v2/user/oauth2/authorize?ui_locales=de&scope=openid%20profile%20email%20phone&response_type=code&client_id=peukiaidm-online-sales&redirect_uri=https://www.kia.com/api/bin/oneid/login&state=default",
        "redirect_pattern": r'^https://.*:8080/api/v1/user/oauth2/redirect',
    },
    "hyundai": {
        "client_id": "6d477c38-3ca4-4cf3-9557-2a1929a94654",
        "client_secret": "KUy49XxPzLpLuoK0xhBC77W6VXhmtQR9iQhmIFjjoY4IpxsV",
        "redirect_url_final": "https://prd.eu-ccapi.hyundai.com:8080/api/v1/user/oauth2/token",
        "success_selector": "button.mail_check",
        "login_url": "https://idpconnect-eu.hyundai.com/auth/api/v2/user/oauth2/authorize?client_id=peuhyundaiidm-ctb&redirect_uri=https%3A%2F%2Fctbapi.hyundai-europe.com%2Fapi%2Fauth&nonce=&state=NL_&scope=openid+profile+email+phone&response_type=code&connector_client_id=peuhyundaiidm-ctb&connector_scope=&connector_session_key=&country=&captcha=1&ui_locales=en-US",
        "redirect_pattern": r'^https://.*:8080/api/v1/user/oauth2/token',
    },
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Bluelink Token Generator</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, sans-serif; max-width: 700px; margin: 40px auto; padding: 0 20px; background: #f5f5f5; }
        .card { background: white; border-radius: 12px; padding: 30px; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        h1 { color: #333; }
        .brand { display: inline-block; padding: 4px 12px; border-radius: 6px; font-weight: bold; color: white; }
        .brand.hyundai { background: #002C5F; }
        .brand.kia { background: #05141F; }
        .btn { display: inline-block; padding: 12px 24px; border-radius: 8px; border: none; color: white; font-size: 16px; cursor: pointer; text-decoration: none; }
        .btn-primary { background: #4CAF50; }
        .btn-primary:hover { background: #45a049; }
        .btn-danger { background: #f44336; }
        .token-box { background: #f0f0f0; padding: 15px; border-radius: 8px; word-break: break-all; font-family: monospace; font-size: 14px; margin: 10px 0; }
        .status { padding: 10px 15px; border-radius: 8px; margin: 15px 0; }
        .status.running { background: #fff3cd; color: #856404; }
        .status.success { background: #d4edda; color: #155724; }
        .status.error { background: #f8d7da; color: #721c24; }
        .info { color: #666; font-size: 14px; }
        .copy-btn { background: #2196F3; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 12px; }
    </style>
</head>
<body>
    <h1>🔑 Bluelink Token Generator</h1>
    <div class="card">
        <p>Brand: <span class="brand {{ brand }}">{{ brand|upper }}</span></p>
        
        {% if status == 'idle' %}
        <p>Klicke auf den Button um den Login-Prozess zu starten. Ein Browser-Fenster wird geöffnet, in dem du dich mit deinen Bluelink-Zugangsdaten anmelden musst.</p>
        <form method="POST" action="/start">
            <button class="btn btn-primary" type="submit">🚀 Token generieren</button>
        </form>
        
        {% elif status == 'waiting_login' %}
        <div class="status running">⏳ Warte auf Login... Bitte melde dich im Browser-Fenster an.</div>
        <p class="info">Das Script wartet bis zu 5 Minuten auf den Login. Die Seite aktualisiert sich automatisch.</p>
        <script>setTimeout(function(){ location.reload(); }, 5000);</script>
        
        {% elif status == 'processing' %}
        <div class="status running">⚙️ Verarbeite Token...</div>
        <script>setTimeout(function(){ location.reload(); }, 3000);</script>
        
        {% elif status == 'success' %}
        <div class="status success">✅ Token erfolgreich generiert!</div>
        <h3>Refresh Token:</h3>
        <div class="token-box" id="refresh">{{ refresh_token }}</div>
        <button class="copy-btn" onclick="navigator.clipboard.writeText(document.getElementById('refresh').innerText)">📋 Kopieren</button>
        
        <h3>Access Token:</h3>
        <div class="token-box" id="access">{{ access_token }}</div>
        <button class="copy-btn" onclick="navigator.clipboard.writeText(document.getElementById('access').innerText)">📋 Kopieren</button>
        
        <p class="info">⚠️ Der Refresh Token ist 180 Tage gültig. Danach muss ein neuer generiert werden.</p>
        <br>
        <form method="POST" action="/reset">
            <button class="btn btn-primary" type="submit">🔄 Neuen Token generieren</button>
        </form>
        
        {% elif status == 'error' %}
        <div class="status error">❌ Fehler: {{ error }}</div>
        <form method="POST" action="/reset">
            <button class="btn btn-danger" type="submit">🔄 Erneut versuchen</button>
        </form>
        {% endif %}
    </div>
    
    <div class="card">
        <h3>Verwendung</h3>
        <p class="info">Verwende den <strong>Refresh Token</strong> als Passwort zusammen mit deinem normalen Benutzernamen bei der Einrichtung der Home Assistant oder evcc Integration.</p>
    </div>
</body>
</html>
"""


def get_token(brand):
    """Run Selenium to get the Bluelink refresh token."""
    global state
    config = BRAND_CONFIG[brand]
    base_url = f"https://idpconnect-eu.{brand}.com/auth/api/v2/user/oauth2/"
    token_url = f"{base_url}token"
    redirect_url = f"{base_url}authorize?response_type=code&client_id={config['client_id']}&redirect_uri={config['redirect_url_final']}&lang=de&state=ccsp"

    driver = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 4.1.1; Galaxy Nexus Build/JRO03C) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19_CCS_APP_AOS")
        # NOT headless - we need the user to interact
        options.add_argument("--remote-debugging-port=9222")

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()

        # Open login page
        state["status"] = "waiting_login"
        driver.get(config["login_url"])

        # Wait for login (5 min timeout)
        wait = WebDriverWait(driver, 300)
        if brand == "kia":
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, config["success_selector"])))
        else:
            wait.until(EC.any_of(
                EC.presence_of_element_located((By.CSS_SELECTOR, config["success_selector"])),
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.ctb_button"))
            ))

        state["status"] = "processing"

        # Redirect to get code
        driver.get(redirect_url)
        time.sleep(3)

        # Wait for redirect with code
        current_url = ""
        for i in range(10):
            current_url = driver.current_url
            if re.match(config["redirect_pattern"], current_url):
                break
            time.sleep(1)

        # Extract code
        code_match = re.search(
            r'code=([0-9a-fA-F-]{36}\.[0-9a-fA-F-]{36}\.[0-9a-fA-F-]{36})',
            current_url
        )
        if not code_match:
            state["status"] = "error"
            state["error"] = f"Konnte keinen Code aus der URL extrahieren: {current_url}"
            return

        code = code_match.group(1)

        # Exchange code for tokens
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": config["redirect_url_final"],
            "client_id": config["client_id"],
            "client_secret": config["client_secret"],
        }

        response = req_lib.post(token_url, data=data)
        if response.status_code == 200:
            tokens = response.json()
            state["refresh_token"] = tokens.get("refresh_token", "N/A")
            state["access_token"] = tokens.get("access_token", "N/A")
            state["status"] = "success"
        else:
            state["status"] = "error"
            state["error"] = f"API Fehler: {response.status_code} - {response.text}"

    except TimeoutException:
        state["status"] = "error"
        state["error"] = "Timeout nach 5 Minuten. Login wurde nicht abgeschlossen."
    except Exception as e:
        state["status"] = "error"
        state["error"] = str(e)
    finally:
        if driver:
            driver.quit()


@app.route("/")
def index():
    brand = os.environ.get("BRAND", "hyundai")
    return render_template_string(
        HTML_TEMPLATE,
        brand=brand,
        status=state["status"],
        refresh_token=state.get("refresh_token"),
        access_token=state.get("access_token"),
        error=state.get("error"),
    )


@app.route("/start", methods=["POST"])
def start():
    brand = os.environ.get("BRAND", "hyundai")
    state["status"] = "waiting_login"
    state["refresh_token"] = None
    state["access_token"] = None
    state["error"] = None
    thread = threading.Thread(target=get_token, args=(brand,))
    thread.daemon = True
    thread.start()
    return render_template_string(
        HTML_TEMPLATE,
        brand=brand,
        status="waiting_login",
        refresh_token=None,
        access_token=None,
        error=None,
    )


@app.route("/reset", methods=["POST"])
def reset():
    state["status"] = "idle"
    state["refresh_token"] = None
    state["access_token"] = None
    state["error"] = None
    from flask import redirect
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9876)
