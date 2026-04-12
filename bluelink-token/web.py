#!/usr/bin/env python3
"""
Bluelink Token Generator - Web Application with Selenium + noVNC
"""

import os
import re
import time
import threading
import subprocess
import requests as req_lib
from flask import Flask, request, jsonify, redirect as flask_redirect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import html as html_lib

app = Flask(__name__)

state = {
    "status": "idle",
    "refresh_token": None,
    "access_token": None,
    "error": None,
    "test_result": "",
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
:root { --primary: #1a73e8; --primary-hover: #1557b0; --success: #188038;
        --success-bg: #e6f4ea; --error: #c5221f; --error-bg: #fce8e6;
        --warning: #b06000; --warning-bg: #fef7e0; --info: #1a73e8;
        --info-bg: #e8f0fe; --text: #202124; --text-secondary: #5f6368;
        --border: #dadce0; --surface: #fff; --bg: #f8f9fa; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Google Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
       background: var(--bg); color: var(--text); min-height: 100vh; }
.header { background: var(--surface); border-bottom: 1px solid var(--border);
          padding: 16px 24px; margin-bottom: 24px; }
.header-inner { max-width: 760px; margin: 0 auto; display: flex;
                align-items: center; gap: 12px; }
.header h1 { font-size: 20px; font-weight: 500; }
.header .brand { font-size: 12px; font-weight: 500; color: var(--text-secondary);
                 background: var(--bg); padding: 2px 10px; border-radius: 12px;
                 border: 1px solid var(--border); text-transform: uppercase;
                 letter-spacing: 0.5px; }
.container { max-width: 760px; margin: 0 auto; padding: 0 24px 40px; }
.card { background: var(--surface); border-radius: 8px; padding: 24px;
        margin-bottom: 16px; border: 1px solid var(--border); }
.card-title { font-size: 16px; font-weight: 500; margin-bottom: 16px; }
.btn { display: inline-flex; align-items: center; gap: 6px; padding: 10px 24px;
       border-radius: 4px; border: none; font-size: 14px; font-weight: 500;
       cursor: pointer; text-decoration: none; transition: all 0.15s;
       font-family: inherit; }
.btn-primary { background: var(--primary); color: white; }
.btn-primary:hover { background: var(--primary-hover); box-shadow: 0 1px 3px rgba(0,0,0,0.2); }
.btn-secondary { background: var(--surface); color: var(--primary);
                 border: 1px solid var(--border); }
.btn-secondary:hover { background: var(--bg); }
.btn-danger { background: var(--surface); color: var(--error);
              border: 1px solid var(--border); }
.btn-danger:hover { background: var(--error-bg); }
.token-label { font-size: 11px; font-weight: 500; color: var(--text-secondary);
               text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px; }
.token-box { background: var(--bg); border: 1px solid var(--border); padding: 14px 16px;
             border-radius: 4px; word-break: break-all; font-family: 'Roboto Mono', monospace;
             font-size: 13px; line-height: 1.6; color: var(--text); }
.copy-link { color: var(--primary); cursor: pointer; font-size: 13px;
             border: none; background: none; font-family: inherit;
             margin-top: 6px; display: inline-block; }
.copy-link:hover { text-decoration: underline; }
.notice { padding: 12px 16px; border-radius: 4px; margin-bottom: 16px;
          font-size: 14px; line-height: 1.5; }
.notice-success { background: var(--success-bg); color: var(--success); }
.notice-error { background: var(--error-bg); color: var(--error); }
.notice-warning { background: var(--warning-bg); color: var(--warning); }
.notice-info { background: var(--info-bg); color: var(--info); }
.divider { border: none; border-top: 1px solid var(--border); margin: 20px 0; }
.actions { display: flex; gap: 8px; flex-wrap: wrap; }
.log { background: #1e1e1e; color: #cccccc; padding: 14px 16px; border-radius: 4px;
       font-family: 'Roboto Mono', monospace; font-size: 12px; max-height: 180px;
       overflow-y: auto; margin: 12px 0; line-height: 1.7; }
.log .ok { color: #4EC9B0; }
.log .warn { color: #dcdcaa; }
.log .err { color: #f48771; }
.vnc-frame { width: 100%; height: 480px; border: 1px solid var(--border);
             border-radius: 4px; margin: 12px 0; background: #000; }
.paste-row { display: flex; gap: 8px; margin-bottom: 4px; }
.paste-row input { flex: 1; padding: 8px 12px; border: 1px solid var(--border);
                   border-radius: 4px; font-size: 14px; font-family: inherit; }
.paste-row input:focus { outline: none; border-color: var(--primary); }
.paste-row button { white-space: nowrap; }
.hint { font-size: 12px; color: var(--text-secondary); margin-top: 4px; line-height: 1.4; }
.section-label { font-size: 13px; font-weight: 500; color: var(--text-secondary);
                 margin-bottom: 8px; }
p { line-height: 1.6; }
"""

SCRIPT = """
function copyToken(id) {
    var text = document.getElementById(id).innerText;
    navigator.clipboard.writeText(text).then(function() {
        var btn = document.querySelector('[data-copy="' + id + '"]');
        var orig = btn.textContent;
        btn.textContent = 'Copied';
        setTimeout(function() { btn.textContent = orig; }, 2000);
    });
}
function sendClipboard() {
    var input = document.getElementById('paste-text');
    var text = input.value;
    if (!text) return;
    fetch('/api/type', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({text: text})
    }).then(function(r) { return r.json(); }).then(function(d) {
        if (d.ok) {
            input.value = '';
            input.placeholder = 'Sent successfully';
            setTimeout(function() { input.placeholder = 'Paste text here...'; }, 2000);
        }
    });
}
"""


def render(content):
    brand = get_brand()
    return f"""<!DOCTYPE html>
<html lang="de"><head>
<title>Bluelink Token Generator</title>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500&family=Roboto+Mono:wght@400&display=swap" rel="stylesheet">
<style>{STYLE}</style></head><body>
<div class="header"><div class="header-inner">
<h1>Bluelink Token Generator</h1>
<span class="brand">{brand}</span>
</div></div>
<div class="container">{content}</div>
<script>{SCRIPT}</script></body></html>"""


def get_brand():
    return os.environ.get("BRAND", "hyundai").lower()


def log(msg, level="info"):
    state["log"].append((level, msg))
    print(f"[{level.upper()}] {msg}")


def format_log():
    lines = []
    for level, msg in state["log"]:
        cls = {"ok": "ok", "warn": "warn", "err": "err"}.get(level, "")
        escaped = html_lib.escape(msg)
        lines.append(f'<span class="{cls}">{escaped}</span>' if cls else escaped)
    return "<br>".join(lines)


def get_token_thread(brand):
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
        log("Starting browser...")

        options = webdriver.ChromeOptions()
        options.binary_location = "/usr/bin/chromium-browser"
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280,800")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Linux; Android 4.1.1; Galaxy Nexus "
            "Build/JRO03C) AppleWebKit/535.19 (KHTML, like Gecko) "
            "Chrome/18.0.1025.166 Mobile Safari/535.19_CCS_APP_AOS")

        service = webdriver.ChromeService(executable_path="/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)

        log(f"Opening {brand.title()} login page...")
        driver.get(config["login_url"])
        log("Waiting for login — please sign in using the browser below.", "warn")

        wait = WebDriverWait(driver, 300)
        if brand == "kia":
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, config["success_selector"])))
        else:
            wait.until(EC.any_of(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, config["success_selector"])),
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "button.ctb_button"))))

        log("Login successful.", "ok")
        state["status"] = "processing"

        log("Retrieving authorization code...")
        driver.get(redirect_url)
        time.sleep(3)

        current_url = ""
        for i in range(15):
            current_url = driver.current_url
            log(f"Waiting for redirect ({i+1}/15)...")
            if re.match(config["code_pattern"], current_url):
                break
            time.sleep(1)

        code_match = re.search(
            r'code=([0-9a-fA-F-]{36}\.[0-9a-fA-F-]{36}\.[0-9a-fA-F-]{36})',
            current_url)
        if not code_match:
            state["status"] = "error"
            state["error"] = f"No auth code found in URL: {current_url[:120]}"
            log(state["error"], "err")
            return

        code = code_match.group(1)
        log("Authorization code received.", "ok")
        log("Exchanging code for token...")

        data = {
            "grant_type": "authorization_code", "code": code,
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
            log("Token generated successfully.", "ok")
        else:
            state["status"] = "error"
            state["error"] = f"API error {response.status_code}: {response.text[:200]}"
            log(state["error"], "err")

    except TimeoutException:
        state["status"] = "error"
        state["error"] = "Timeout — login was not completed within 5 minutes."
        log(state["error"], "err")
    except Exception as e:
        state["status"] = "error"
        state["error"] = str(e)
        log(f"Error: {e}", "err")
    finally:
        if driver:
            try: driver.quit()
            except Exception: pass
        log("Browser closed.")


# ── Routes ──────────────────────────────────────────────────

@app.route("/")
def index():
    brand = get_brand()
    bt = brand.title()
    s = state["status"]

    if s == "idle":
        return render(f"""
<div class="card">
    <div class="card-title">Generate Refresh Token</div>
    <p style="margin-bottom: 16px; color: var(--text-secondary); font-size: 14px;">
        A Chromium browser will open in the background. You can interact with it
        through the embedded viewer below to complete the {bt} Bluelink login.
    </p>
    <form method="POST" action="/start">
        <button type="submit" class="btn btn-primary">Start token generation</button>
    </form>
</div>""")

    elif s == "waiting_login":
        return render(f"""
<div class="card">
    <div class="card-title">Sign in to {bt} Bluelink</div>
    <div class="notice notice-warning">
        Waiting for login. Use your {bt} Bluelink credentials (same as the mobile app).
        The session will time out after 5 minutes.
    </div>
    <div class="log" id="log-box">{format_log()}</div>
    <hr class="divider">
    <div class="section-label">Paste text into browser</div>
    <div class="paste-row">
        <input type="text" id="paste-text" placeholder="Paste text here (e.g. password)..."
               onkeydown="if(event.key==='Enter')sendClipboard()">
        <button class="btn btn-secondary" onclick="sendClipboard()">Send</button>
    </div>
    <p class="hint">Click into the input field in the browser below first, then paste your text above and press Send.</p>
    <hr class="divider">
    <div class="section-label">Remote browser</div>
    <iframe src="/novnc" class="vnc-frame" id="vnc"></iframe>
</div>
<script>
(function poll() {{
    fetch('/api/status').then(function(r){{ return r.json(); }}).then(function(d) {{
        document.getElementById('log-box').innerHTML = d.log;
        if (d.status !== 'waiting_login') location.reload();
        else setTimeout(poll, 3000);
    }}).catch(function(){{ setTimeout(poll, 3000); }});
}})();
</script>""")

    elif s == "processing":
        return render(f"""
<div class="card">
    <div class="card-title">Processing</div>
    <div class="notice notice-info">Login successful. Retrieving token...</div>
    <div class="log" id="log-box">{format_log()}</div>
</div>
<script>
(function poll() {{
    fetch('/api/status').then(function(r){{ return r.json(); }}).then(function(d) {{
        document.getElementById('log-box').innerHTML = d.log;
        if (d.status !== 'processing') location.reload();
        else setTimeout(poll, 2000);
    }}).catch(function(){{ setTimeout(poll, 2000); }});
}})();
</script>""")

    elif s == "success":
        rt = html_lib.escape(state.get("refresh_token", ""))
        tr = state.get("test_result", "")
        test_html = ""
        if tr == "ok":
            test_html = '<div class="notice notice-success">Token verified — API connection successful.</div>'
        elif tr:
            test_html = f'<div class="notice notice-error">Verification failed: {html_lib.escape(tr)}</div>'
        return render(f"""
<div class="card">
    <div class="card-title">Token generated</div>
    <div class="notice notice-success">The refresh token was generated successfully.</div>
    {test_html}
    <div style="margin: 20px 0;">
        <div class="token-label">Refresh Token</div>
        <div class="token-box" id="refresh">{rt}</div>
        <button class="copy-link" data-copy="refresh" onclick="copyToken('refresh')">Copy to clipboard</button>
    </div>
    <div class="notice notice-warning">
        This token is valid for 180 days. After that you will need to generate a new one.
    </div>
    <hr class="divider">
    <p style="font-size: 14px; color: var(--text-secondary); margin-bottom: 16px;">
        Use this refresh token as the password together with your regular username
        when configuring the evcc or Home Assistant integration.
    </p>
    <div class="actions">
        <form method="POST" action="/test" style="margin:0;">
            <button type="submit" class="btn btn-secondary">Verify token</button>
        </form>
        <form method="POST" action="/reset" style="margin:0;">
            <button type="submit" class="btn btn-danger">Generate new token</button>
        </form>
    </div>
    <hr class="divider">
    <details><summary style="cursor:pointer; font-size:13px; color:var(--text-secondary);">Show log</summary>
    <div class="log">{format_log()}</div></details>
</div>""")

    elif s == "error":
        err = html_lib.escape(state.get("error", "Unknown error"))
        return render(f"""
<div class="card">
    <div class="card-title">Error</div>
    <div class="notice notice-error">{err}</div>
    <details open><summary style="cursor:pointer; font-size:13px; color:var(--text-secondary);">Log</summary>
    <div class="log">{format_log()}</div></details>
    <hr class="divider">
    <form method="POST" action="/reset">
        <button type="submit" class="btn btn-primary">Try again</button>
    </form>
</div>""")

    return render('<div class="card">Unknown state</div>')


@app.route("/start", methods=["POST"])
def start():
    brand = get_brand()
    state.update({"status": "waiting_login", "refresh_token": None,
                  "access_token": None, "error": None, "test_result": "", "log": []})
    threading.Thread(target=get_token_thread, args=(brand,), daemon=True).start()
    return render("""
<div class="card">
    <div class="notice notice-info">Starting browser... redirecting shortly.</div>
</div>
<script>setTimeout(function(){ location.href = '/'; }, 2000);</script>""")


@app.route("/reset", methods=["POST"])
def reset():
    state.update({"status": "idle", "refresh_token": None, "access_token": None,
                  "error": None, "test_result": "", "log": []})
    return flask_redirect("/")


@app.route("/novnc")
def novnc():
    host = request.host.split(":")[0]
    return (f'<!DOCTYPE html><html><head>'
            f'<meta http-equiv="refresh" content="0;url=http://{host}:6080/vnc.html?autoconnect=true&resize=scale">'
            f'</head><body></body></html>')


@app.route("/test", methods=["POST"])
def test_token():
    brand = get_brand()
    config = BRAND_CONFIG[brand]
    access_token = state.get("access_token")
    refresh_token = state.get("refresh_token")

    if not access_token:
        state["test_result"] = "No access token available."
        return flask_redirect("/")

    token_url = f"{config['base_url']}/token"
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        api_url = (f"https://prd.eu-ccapi.{brand}.com:8080"
                   f"/api/v1/spa/notifications")
        response = req_lib.get(api_url, headers=headers, timeout=10)

        if response.status_code == 200:
            state["test_result"] = "ok"
        elif response.status_code == 401:
            data = {"grant_type": "refresh_token", "refresh_token": refresh_token,
                    "client_id": config["client_id"], "client_secret": config["client_secret"]}
            rr = req_lib.post(token_url, data=data, timeout=10)
            if rr.status_code == 200:
                state["access_token"] = rr.json().get("access_token", access_token)
                state["test_result"] = "ok"
            else:
                state["test_result"] = f"Refresh failed ({rr.status_code})"
        else:
            state["test_result"] = f"API returned {response.status_code}"
    except Exception as e:
        state["test_result"] = str(e)

    return flask_redirect("/")


@app.route("/api/type", methods=["POST"])
def api_type():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"ok": False, "error": "No text"})
    try:
        subprocess.run(
            ["xdotool", "type", "--clearmodifiers", "--delay", "50", text],
            env={**os.environ, "DISPLAY": ":99"}, timeout=10)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})


@app.route("/api/status")
def api_status():
    return jsonify({"status": state["status"], "log": format_log()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9876)
