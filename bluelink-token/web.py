#!/usr/bin/env python3
"""
Bluelink Token Generator - Web Application with Selenium + noVNC
The user can watch and interact with the browser via noVNC.
"""

import os
import re
import time
import threading
import requests as req_lib
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import html as html_lib

app = Flask(__name__)

state = {
    "status": "idle",  # idle, waiting_login, processing, success, error
    "refresh_token": None,
    "access_token": None,
    "error": None,
    "log": [],
}

BRAND_CONFIG = {
    "kia": {
        "client_id": "fdc85c00-0a2f-4c64-bcb4-2cfb1500730a",
        "client_secret": "secret",
        "base_url": "https://idpconnect-eu.kia.com/auth/api/v2/user/oauth2",
        "redirect_url_final": "https://prd.eu-ccapi.kia.com:8080/api/v1/user/oauth2/redirect",
        "login_url": "https://idpconnect-eu.kia.com/auth/api/v2/user/oauth2/authorize?ui_locales=de&scope=openid%20profile%20email%20phone&response_type=code&client_id=peukiaidm-online-sales&redirect_uri=https%3A%2F%2Fwww.kia.com%2Fapi%2Fbin%2Foneid%2Flogin&state=aHR0cHM6Ly93d3cua2lhLmNvbTo0NDMvZGUvP21zb2NraWQ9MjM1NDU0ODBmNmUyNjg5NDIwMmU0MDBjZjc2OTY5NWQmX3RtPTE3NTYzMTg3MjY1OTImX3RtPTE3NTYzMjQyMTcxMjY%3D_default",
        "success_selector": "a[class='logout user']",
        "code_pattern": r'^https://.*:8080/api/v1/user/oauth2/redirect',
    },
    "hyundai": {
        "client_id": "6d477c38-3ca4-4cf3-9557-2a1929a94654",
        "client_secret": "KUy49XxPzLpLuoK0xhBC77W6VXhmtQR9iQhmIFjjoY4IpxsV",
        "base_url": "https://idpconnect-eu.hyundai.com/auth/api/v2/user/oauth2",
        "redirect_url_final": "https://prd.eu-ccapi.hyundai.com:8080/api/v1/user/oauth2/token",
        "login_url": "https://idpconnect-eu.hyundai.com/auth/api/v2/user/oauth2/authorize?client_id=peuhyundaiidm-ctb&redirect_uri=https%3A%2F%2Fctbapi.hyundai-europe.com%2Fapi%2Fauth&nonce=&state=NL_&scope=openid+profile+email+phone&response_type=code&connector_client_id=peuhyundaiidm-ctb&connector_scope=&connector_session_key=&country=&captcha=1&ui_locales=en-US",
        "success_selector": "button.mail_check",
        "code_pattern": r'^https://.*:8080/api/v1/user/oauth2/token',
    },
}

STYLE = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
       background: #f0f2f5; color: #333; min-height: 100vh; padding: 20px; }
.container { max-width: 700px; margin: 0 auto; }
h1 { font-size: 24px; margin-bottom: 8px; }
.subtitle { color: #666; margin-bottom: 24px; }
.card { background: white; border-radius: 12px; padding: 24px;
        margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.brand-badge { display: inline-block; padding: 4px 14px; border-radius: 20px;
               font-weight: 600; font-size: 13px; color: white; margin-bottom: 16px; }
.brand-badge.hyundai { background: #002C5F; }
.brand-badge.kia { background: #05141F; }
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
.log { background: #1e1e1e; color: #d4d4d4; padding: 12px; border-radius: 8px;
       font-family: monospace; font-size: 12px; max-height: 200px; overflow-y: auto;
       margin: 12px 0; line-height: 1.6; }
.log .ok { color: #4EC9B0; }
.log .warn { color: #CE9178; }
.log .err { color: #F44747; }
.vnc-frame { width: 100%; height: 500px; border: 1px solid #ddd; border-radius: 8px;
             margin: 12px 0; }
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


def log(msg, level="info"):
    state["log"].append((level, msg))
    print(f"[{level.upper()}] {msg}")


def get_token_thread(brand):
    """Run the full Selenium flow to get tokens."""
    config = BRAND_CONFIG[brand]
    base_url = config["base_url"]
    token_url = f"{base_url}/token"
    redirect_url = (f"{base_url}/authorize?"
                    f"response_type=code&client_id={config['client_id']}"
                    f"&redirect_uri={config['redirect_url_final']}"
                    f"&lang=de&state=ccsp")

    driver = None
    try:
        state["status"] = "waiting_login"
        state["log"] = []
        log("Starte Chromium Browser...")

        options = webdriver.ChromeOptions()
        options.binary_location = "/usr/bin/chromium-browser"
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280,800")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Linux; Android 4.1.1; Galaxy Nexus "
            "Build/JRO03C) AppleWebKit/535.19 (KHTML, like Gecko) "
            "Chrome/18.0.1025.166 Mobile Safari/535.19_CCS_APP_AOS"
        )

        service = webdriver.ChromeService(executable_path="/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)

        log(f"Öffne {brand.title()} Login-Seite...")
        driver.get(config["login_url"])
        log("Warte auf Login... Bitte im noVNC-Fenster anmelden!", "warn")

        wait = WebDriverWait(driver, 300)
        if brand == "kia":
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, config["success_selector"])))
        else:
            wait.until(EC.any_of(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, config["success_selector"])),
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "button.ctb_button"))
            ))

        log("Login erfolgreich!", "ok")
        state["status"] = "processing"

        log("Hole Autorisierungscode...")
        driver.get(redirect_url)
        time.sleep(3)

        current_url = ""
        for i in range(15):
            current_url = driver.current_url
            log(f"Warte auf Redirect... ({i+1}/15)")
            if re.match(config["code_pattern"], current_url):
                break
            time.sleep(1)

        code_match = re.search(
            r'code=([0-9a-fA-F-]{36}\.[0-9a-fA-F-]{36}\.[0-9a-fA-F-]{36})',
            current_url
        )
        if not code_match:
            state["status"] = "error"
            state["error"] = f"Kein Auth-Code in URL gefunden: {current_url[:100]}"
            log(state["error"], "err")
            return

        code = code_match.group(1)
        log("Auth-Code erhalten!", "ok")

        log("Tausche Code gegen Token...")
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": config["redirect_url_final"],
            "client_id": config["client_id"],
            "client_secret": config["client_secret"],
        }
        response = req_lib.post(token_url, data=data, timeout=15)

        if response.status_code == 200:
            tokens = response.json()
            state["refresh_token"] = tokens.get("refresh_token", "N/A")
            state["access_token"] = tokens.get("access_token", "N/A")
            state["status"] = "success"
            log("Token erfolgreich generiert!", "ok")
        else:
            state["status"] = "error"
            state["error"] = f"API Fehler {response.status_code}: {response.text[:200]}"
            log(state["error"], "err")

    except TimeoutException:
        state["status"] = "error"
        state["error"] = "Timeout nach 5 Minuten. Login wurde nicht abgeschlossen."
        log(state["error"], "err")
    except Exception as e:
        state["status"] = "error"
        state["error"] = str(e)
        log(f"Fehler: {e}", "err")
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass
        log("Browser geschlossen.")


def format_log():
    lines = []
    for level, msg in state["log"]:
        cls = {"ok": "ok", "warn": "warn", "err": "err"}.get(level, "")
        escaped = html_lib.escape(msg)
        if cls:
            lines.append(f'<span class="{cls}">{escaped}</span>')
        else:
            lines.append(escaped)
    return "<br>".join(lines)


@app.route("/")
def index():
    brand = get_brand()
    bt = brand.title()
    s = state["status"]

    if s == "idle":
        return render(f"""
<div class="card">
    <span class="brand-badge {brand}">{brand.upper()}</span>
    <p style="margin-bottom: 16px;">Generiere einen Refresh Token für dein {bt} Fahrzeug.</p>
    <p style="margin-bottom: 16px; font-size: 14px;">
        Nach dem Klick auf "Starten" öffnet sich ein Browser im Hintergrund.
        Du kannst den Browser über das <strong>noVNC-Fenster</strong> unten sehen und dich dort anmelden.
    </p>
    <form method="POST" action="/start">
        <button type="submit" class="btn btn-primary">🚀 Token-Generierung starten</button>
    </form>
</div>
<div class="card">
    <div class="alert alert-info">💡 Marke ändern: Addon-Konfiguration → brand → hyundai oder kia</div>
</div>""")

    elif s == "waiting_login":
        return render(f"""
<div class="card">
    <span class="brand-badge {brand}">{brand.upper()}</span>
    <div class="alert alert-warning">
        ⏳ Warte auf Login... Bitte melde dich im Browser-Fenster unten an!
    </div>
    <p style="margin-bottom: 12px; font-size: 14px;">
        Verwende deine {bt} Bluelink-Zugangsdaten (die gleichen wie in der App).
        Das Script wartet bis zu 5 Minuten.
    </p>
    <div class="log">{format_log()}</div>
    <hr class="divider">
    <h3 style="margin-bottom: 8px;">Browser (noVNC)</h3>
    <iframe src="/novnc" class="vnc-frame"></iframe>
    <p style="font-size: 12px; color: #999; margin-top: 4px;">
        Falls das Fenster leer ist, warte einen Moment und lade die Seite neu.
    </p>
</div>
<script>setTimeout(function(){{ location.reload(); }}, 5000);</script>""")

    elif s == "processing":
        return render(f"""
<div class="card">
    <span class="brand-badge {brand}">{brand.upper()}</span>
    <div class="alert alert-info">⚙️ Login erfolgreich! Verarbeite Token...</div>
    <div class="log">{format_log()}</div>
</div>
<script>setTimeout(function(){{ location.reload(); }}, 3000);</script>""")

    elif s == "success":
        rt = html_lib.escape(state.get("refresh_token", ""))
        at = html_lib.escape(state.get("access_token", ""))
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
    <div class="alert alert-warning">⚠️ Der Refresh Token ist <strong>180 Tage</strong> gültig.</div>
    <hr class="divider">
    <p style="font-size: 14px; color: #666;">
        Verwende den <strong>Refresh Token</strong> als Passwort zusammen mit deinem
        normalen Benutzernamen bei der Einrichtung der evcc oder Home Assistant Integration.
    </p>
    <div class="log">{format_log()}</div>
    <hr class="divider">
    <form method="POST" action="/reset">
        <button type="submit" class="btn btn-outline">🔄 Neuen Token generieren</button>
    </form>
</div>""")

    elif s == "error":
        err = html_lib.escape(state.get("error", "Unbekannter Fehler"))
        return render(f"""
<div class="card">
    <span class="brand-badge {brand}">{brand.upper()}</span>
    <div class="alert alert-error">❌ {err}</div>
    <div class="log">{format_log()}</div>
    <hr class="divider">
    <form method="POST" action="/reset">
        <button type="submit" class="btn btn-primary">🔄 Erneut versuchen</button>
    </form>
</div>""")

    return render('<div class="card">Unbekannter Status</div>')


@app.route("/start", methods=["POST"])
def start():
    brand = get_brand()
    state["status"] = "waiting_login"
    state["refresh_token"] = None
    state["access_token"] = None
    state["error"] = None
    state["log"] = []
    t = threading.Thread(target=get_token_thread, args=(brand,), daemon=True)
    t.start()
    return render(f"""
<div class="card">
    <div class="alert alert-info">⚙️ Browser wird gestartet... Seite lädt gleich neu.</div>
</div>
<script>setTimeout(function(){{ location.href = '/'; }}, 2000);</script>""")


@app.route("/reset", methods=["POST"])
def reset():
    state["status"] = "idle"
    state["refresh_token"] = None
    state["access_token"] = None
    state["error"] = None
    state["log"] = []
    return render("""
<div class="card"><div class="alert alert-info">Zurückgesetzt.</div></div>
<script>setTimeout(function(){ location.href = '/'; }, 1000);</script>""")


@app.route("/novnc")
def novnc():
    """Redirect to noVNC client."""
    host = request.host.split(":")[0]
    return f"""<!DOCTYPE html><html><head>
<meta http-equiv="refresh" content="0;url=http://{host}:6080/vnc.html?autoconnect=true&resize=scale">
</head><body>Redirecting to noVNC...</body></html>"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9876)
