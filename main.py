import os
import time
import json
import urllib.request
import urllib.error
import threading
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 10000))
ADMIN_SECRET = os.environ.get("ADMIN_SECRET", "Lipan8908@")
START_TIME = time.time()

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8888310796:AAE8vPg6DC-RcSxZb1YKYm_EiIxwtCjObAM")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "7198790563")

FREELLM_KEY = os.environ.get("FREELLM_KEY", "sk-cp-9b5527df917c6e6463295c54976b382c027519fab2d12768")

SERVICES = [
    {
        "id": "nanobot-master",
        "name": "Nanobot Master (Chief AI)",
        "account": "infinitycheats900@gmail.com",
        "url": os.environ.get("URL_NANOBOT", "https://nanobot-ai-assistant.onrender.com/health"),
        "srv_id": os.environ.get("SRV_NANOBOT", "srv-dbp2g015efls739742sg"),
        "token": os.environ.get("TOK_NANOBOT", "rnd_68NvuTzjBCTs1A3eIgPT28Jd8UAo"),
        "consecutive_fails": 0,
        "status": "starting",
        "latency_ms": 0,
        "last_checked": 0,
        "restarts": 0
    },
    {
        "id": "freellm-gateway",
        "name": "FreeLLMAPI Unified Gateway",
        "account": "silentx7894@gmail.com",
        "url": os.environ.get("URL_FREELLM", "https://freellmapi-dab8.onrender.com/"),
        "srv_id": os.environ.get("SRV_FREELLM", "srv-dbqaqpjm8hqs73a9mrpg"),
        "token": os.environ.get("TOK_FREELLM", "rnd_9uAnDiiU73twVZe1F1E2E2nc899G"),
        "consecutive_fails": 0,
        "status": "starting",
        "latency_ms": 0,
        "last_checked": 0,
        "restarts": 0
    },
    {
        "id": "picoclaw-worker-1",
        "name": "Worker 1: Browser-Use & Web Actions",
        "account": "kumarjenarajesh780@gmail.com",
        "url": os.environ.get("URL_WORKER1", "https://picoclaw-worker-1.onrender.com/health"),
        "srv_id": os.environ.get("SRV_WORKER1", "srv-dbqd2bqjnfac738b0mf0"),
        "token": os.environ.get("TOK_WORKER1", "rnd_v8efKcq2qdCjyrE8xptSLy4OjrSx"),
        "consecutive_fails": 0,
        "status": "starting",
        "latency_ms": 0,
        "last_checked": 0,
        "restarts": 0
    },
    {
        "id": "picoclaw-worker-2",
        "name": "Worker 2: Heavy Coder Runner",
        "account": "lopitasubhadarshinee6068@gmail.com",
        "url": os.environ.get("URL_WORKER2", "https://picoclaw-worker-2.onrender.com/health"),
        "srv_id": os.environ.get("SRV_WORKER2", "srv-dbqd7v8n74is73brket0"),
        "token": os.environ.get("TOK_WORKER2", "rnd_nHK3QeRR4vuKH80XZhz30yxnn5I1"),
        "consecutive_fails": 0,
        "status": "starting",
        "latency_ms": 0,
        "last_checked": 0,
        "restarts": 0
    },
    {
        "id": "picoclaw-worker-3",
        "name": "Worker 3: Web Scraper & Deal Sniper",
        "account": "moharanalipankumar123@gmail.com",
        "url": os.environ.get("URL_WORKER3", "https://picoclaw-worker-3.onrender.com/health"),
        "srv_id": os.environ.get("SRV_WORKER3", "srv-dbqd80mi0phs73cb5h8g"),
        "token": os.environ.get("TOK_WORKER3", "rnd_9kw6oboxHgUPA2idJIpGP8Tl6IKU"),
        "consecutive_fails": 0,
        "status": "starting",
        "latency_ms": 0,
        "last_checked": 0,
        "restarts": 0
    },
    {
        "id": "picoclaw-worker-4",
        "name": "Worker 4: Media & Reels Downloader",
        "account": "krutibas7894@gmail.com",
        "url": os.environ.get("URL_WORKER4", "https://picoclaw-worker-4.onrender.com/health"),
        "srv_id": os.environ.get("SRV_WORKER4", "srv-dbqd818ae00c7382fkf0"),
        "token": os.environ.get("TOK_WORKER4", "rnd_5yNpVpPqbenzfy4ugOFS3Ny7z50D"),
        "consecutive_fails": 0,
        "status": "starting",
        "latency_ms": 0,
        "last_checked": 0,
        "restarts": 0
    },
    {
        "id": "picoclaw-worker-5",
        "name": "Worker 5: Lipan Personal PicoClaw Assistant (@lipan_apex_bot)",
        "account": "lipan.personal@gmail.com",
        "url": os.environ.get("URL_WORKER5", "https://picoclaw-worker-5.onrender.com/health"),
        "srv_id": os.environ.get("SRV_WORKER5", "srv-dbqd82tg1s2s73e0991g"),
        "token": os.environ.get("TOK_WORKER5", "rnd_bTscBhBOWGRtwhZd24jJfFXAtTJ3"),
        "consecutive_fails": 0,
        "status": "starting",
        "latency_ms": 0,
        "last_checked": 0,
        "restarts": 0
    },
    {
        "id": "alpine-webtop",
        "name": "Worker 6: Alpine Linux Cloud Desktop (Webtop)",
        "account": "silentxop8908@gmail.com",
        "url": os.environ.get("URL_WORKER6", "https://alpine-webtop.onrender.com/health"),
        "srv_id": os.environ.get("SRV_WORKER6", "srv-dbrkriu7bikc73aqu7bg"),
        "token": os.environ.get("TOK_WORKER6", "rnd_kN4R27A9gB7xkt9Rf6ioMftEVNBY"),
        "consecutive_fails": 0,
        "status": "starting",
        "latency_ms": 0,
        "last_checked": 0,
        "restarts": 0
    },
    {
        "id": "taraprasad-picoclaw",
        "name": "Taraprasad PicoClaw (@TaraPrimeBot)",
        "account": "jiatiku74@gmail.com",
        "url": os.environ.get("URL_TARAPRASAD_PICOCLAW", "https://picoclaw-taraprasad.onrender.com/health"),
        "srv_id": os.environ.get("SRV_TARAPRASAD_PICOCLAW", "srv-dbrcg95g1s2s7383gji0"),
        "token": os.environ.get("TOK_TARAPRASAD_PICOCLAW", "rnd_n12Drzx2PbQEW5XZ3fnAMgcC9UHa"),
        "consecutive_fails": 0,
        "status": "starting",
        "latency_ms": 0,
        "last_checked": 0,
        "restarts": 0
    },
    {
        "id": "taraprasad-freellm",
        "name": "Taraprasad FreeLLM Gateway",
        "account": "sonenadelt@gmail.com",
        "url": os.environ.get("URL_TARAPRASAD_FREELLM", "https://freellm-taraprasad.onrender.com/api/ping"),
        "srv_id": os.environ.get("SRV_TARAPRASAD_FREELLM", "srv-dbrcovl9fdbs73e0idr0"),
        "token": os.environ.get("TOK_TARAPRASAD_FREELLM", "rnd_UD3w4qYiyk8aW4k0NuTx1zxPBUTG"),
        "api_key": "freellmapi-54f868a9d1283274a6bb2fedd4f0a5efec7afc694da8e586",
        "consecutive_fails": 0,
        "status": "starting",
        "latency_ms": 0,
        "last_checked": 0,
        "restarts": 0
    }
]

def send_telegram_alert(msg: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"[Alert Error] {e}")

def trigger_restart(s):
    if not s.get("srv_id") or not s.get("token"):
        return False, "Missing service ID or token"
    
    url = f"https://api.render.com/v1/services/{s['srv_id']}/restart"
    req = urllib.request.Request(
        url,
        data=b"{}",
        headers={"Authorization": f"Bearer {s['token']}", "Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            s["restarts"] += 1
            s["consecutive_fails"] = 0
            s["status"] = "restarting"
            alert_msg = f"🏥 *The Doctor Alert*\n\n⚡ *Node:* `{s['name']}`\n🔄 *Action:* Render Service Restart Triggered (`{s['srv_id']}`)\n📊 *Total Restarts:* {s['restarts']}"
            send_telegram_alert(alert_msg)
            print(f"✓ Triggered restart for {s['name']}")
            return True, "Restart initiated"
    except Exception as e:
        # Fallback to trigger deploy if restart endpoint fails
        try:
            dep_url = f"https://api.render.com/v1/services/{s['srv_id']}/deploys"
            dep_req = urllib.request.Request(
                dep_url,
                data=json.dumps({"clearCache": "do_not_clear"}).encode("utf-8"),
                headers={"Authorization": f"Bearer {s['token']}", "Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(dep_req, timeout=10) as resp:
                s["restarts"] += 1
                s["consecutive_fails"] = 0
                s["status"] = "restarting"
                return True, "Redeploy initiated"
        except Exception as e2:
            print(f"Error restarting {s['name']}: {e2}")
            return False, str(e2)

def check_services():
    for s in SERVICES:
        t0 = time.time()
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) TheDoctorSentry/2.0"}
        if "freellm" in s["id"]:
            headers["Authorization"] = f"Bearer {s.get('api_key', FREELLM_KEY)}"
            
        req = urllib.request.Request(s["url"], headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=8) as resp:
                latency = round((time.time() - t0) * 1000, 1)
                s["latency_ms"] = latency
                s["last_checked"] = int(time.time())
                
                was_failing = s["consecutive_fails"] >= 3
                s["consecutive_fails"] = 0
                s["status"] = "healthy"
                
                if was_failing:
                    send_telegram_alert(f"✅ *Node Recovered*\n\nNode `{s['name']}` is now back online and *HEALTHY* (Latency: {latency}ms).")
                    
        except Exception as e:
            s["latency_ms"] = -1
            s["consecutive_fails"] += 1
            s["status"] = "degraded" if s["consecutive_fails"] < 3 else "offline"
            print(f"[Doctor] Warning: {s['name']} check failed ({s['consecutive_fails']}/3): {e}")
            
            if s["consecutive_fails"] == 3:
                alert = f"🚨 *CRITICAL SENTRY ALERT*\n\nNode `{s['name']}` failed 3 consecutive health checks!\nError: `{e}`\n\n🏥 *Action:* Doctor is auto-restarting the container now..."
                send_telegram_alert(alert)
                trigger_restart(s)

def watchdog_loop():
    print(f"🏥 The Doctor Watchdog Active: 24/7 Monitoring {len(SERVICES)} Nodes...")
    while True:
        try:
            check_services()
        except Exception as e:
            print(f"[Watchdog Loop Exception] {e}")
        time.sleep(30)

class RequestHandler(BaseHTTPRequestHandler):
    def check_auth(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        
        # 1. Query parameter: ?secret=...
        if qs.get("secret", [""])[0] == ADMIN_SECRET:
            return True
            
        # 2. Cookie: sentry_secret=...
        cookie_header = self.headers.get("Cookie", "")
        if f"sentry_secret={ADMIN_SECRET}" in cookie_header:
            return True
            
        # 3. Header: Authorization: Bearer ...
        auth_header = self.headers.get("Authorization", "")
        if auth_header == f"Bearer {ADMIN_SECRET}":
            return True
            
        return False

    def send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def render_lock_screen(self):
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔒 Access Restricted - The Doctor</title>
    <style>
        body {{
            background: #090d16;
            color: #f3f4f6;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }}
        .box {{
            background: #111827;
            border: 1px solid #1f2937;
            border-radius: 16px;
            padding: 32px;
            width: 100%;
            max-width: 400px;
            text-align: center;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        }}
        .icon {{ font-size: 48px; margin-bottom: 16px; }}
        h2 {{ margin: 0 0 8px; font-size: 20px; color: #38bdf8; }}
        p {{ margin: 0 0 24px; font-size: 13px; color: #94a3b8; }}
        input {{
            width: 100%;
            box-sizing: border-box;
            background: #090d16;
            border: 1px solid #334155;
            color: #fff;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 14px;
            outline: none;
            margin-bottom: 16px;
            transition: border-color 0.2s;
        }}
        input:focus {{ border-color: #38bdf8; }}
        button {{
            width: 100%;
            background: #0284c7;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }}
        button:hover {{ background: #0369a1; }}
        .badge {{
            display: inline-block;
            margin-top: 16px;
            font-size: 11px;
            color: #64748b;
        }}
    </style>
</head>
<body>
    <div class="box">
        <div class="icon">🔒</div>
        <h2>THE DOCTOR SENTRY</h2>
        <p>Restricted Command Center · Multi-Agent Swarm</p>
        <input type="password" id="secretInput" placeholder="Enter Admin Secret..." autofocus />
        <button onclick="login()">Unlock Dashboard</button>
        <div class="badge">Protected by Antigravity Defense Protocol</div>
    </div>
    <script>
        function login() {{
            const val = document.getElementById("secretInput").value.trim();
            if (!val) return;
            document.cookie = "sentry_secret=" + encodeURIComponent(val) + "; path=/; max-age=2592000; SameSite=Lax";
            window.location.href = window.location.pathname + "?secret=" + encodeURIComponent(val);
        }}
        document.getElementById("secretInput").addEventListener("keypress", function(e) {{
            if (e.key === "Enter") login();
        }});
    </script>
</body>
</html>"""
        self.send_response(401)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def render_dashboard(self):
        uptime = int(time.time() - START_TIME)
        days = uptime // 86400
        hrs = (uptime % 86400) // 3600
        mins = (uptime % 3600) // 60
        uptime_str = f"{days}d {hrs}h {mins}m" if days else (f"{hrs}h {mins}m" if hrs else f"{uptime}s")

        cards_html = ""
        for s in SERVICES:
            badge_color = "#10b981" if s["status"] == "healthy" else ("#f59e0b" if s["status"] in ("starting", "restarting") else "#ef4444")
            status_text = s["status"].upper()
            latency_text = f"{s['latency_ms']} ms" if s['latency_ms'] >= 0 else "FAIL"
            
            # Mask URL for security
            parsed_u = urlparse(s["url"])
            domain = parsed_u.netloc
            masked_domain = domain[:4] + "***" + domain[-12:] if len(domain) > 16 else domain
            masked_url = f"{parsed_u.scheme}://{masked_domain}{parsed_u.path}"

            cards_html += f"""
            <div class="card" id="card-{s['id']}">
                <div class="card-header">
                    <span class="dot" style="background: {badge_color};"></span>
                    <span class="card-title">{s['name']}</span>
                </div>
                <div class="card-meta">
                    <div><b>Status:</b> <span id="status-{s['id']}" style="color: {badge_color}; font-weight: 600;">{status_text}</span></div>
                    <div><b>Latency:</b> <span id="latency-{s['id']}">{latency_text}</span></div>
                    <div><b>Account:</b> <span style="color: #94a3b8; font-size: 11px;">{s['account']}</span></div>
                    <div><b>Restarts:</b> <span id="restarts-{s['id']}">{s['restarts']}</span></div>
                    <div class="url-row">
                        <span class="masked-url" id="url-{s['id']}">{masked_url}</span>
                        <span class="full-url" style="display: none;" id="fullurl-{s['id']}">{s['url']}</span>
                    </div>
                </div>
                <div class="card-actions">
                    <button class="btn-restart" id="btn-{s['id']}" onclick="restartNode('{s['id']}')">🔄 Restart Node</button>
                    <button class="btn-ping" onclick="pingNode('{s['id']}')">⚡ Ping</button>
                </div>
            </div>
            """

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏥 The Doctor - Multi-Agent Swarm Command Center</title>
    <style>
        body {{
            background: #090d16;
            color: #f3f4f6;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 24px;
        }}
        .header {{
            max-width: 1100px;
            margin: 0 auto 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #1f2937;
            padding-bottom: 16px;
            flex-wrap: wrap;
            gap: 12px;
        }}
        .title {{ font-size: 22px; font-weight: 700; color: #38bdf8; display: flex; align-items: center; gap: 10px; }}
        .header-controls {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
        .badge {{ background: #1e293b; padding: 6px 14px; border-radius: 9999px; font-size: 12px; color: #94a3b8; border: 1px solid #334155; }}
        .quota-badge {{ background: #064e3b; color: #34d399; border: 1px solid #059669; padding: 6px 14px; border-radius: 9999px; font-size: 12px; font-weight: 600; }}
        
        .toolbar {{
            max-width: 1100px;
            margin: 0 auto 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #111827;
            padding: 12px 16px;
            border-radius: 10px;
            border: 1px solid #1f2937;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .btn-tool {{
            background: #1e293b;
            color: #f3f4f6;
            border: 1px solid #334155;
            padding: 8px 14px;
            border-radius: 6px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-tool:hover {{ background: #334155; border-color: #38bdf8; }}
        .btn-primary {{
            background: #0284c7;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }}
        .btn-primary:hover {{ background: #0369a1; }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 16px;
            max-width: 1100px;
            margin: 0 auto;
        }}
        .card {{
            background: #111827;
            border: 1px solid #1f2937;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s, border-color 0.2s;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .card:hover {{ border-color: #38bdf8; transform: translateY(-2px); }}
        .card-header {{ display: flex; align-items: center; gap: 10px; margin-bottom: 12px; font-weight: 600; font-size: 15px; }}
        .dot {{ width: 10px; height: 10px; border-radius: 50%; box-shadow: 0 0 8px currentColor; }}
        .card-meta {{ font-size: 13px; color: #9ca3af; line-height: 1.8; margin-bottom: 14px; }}
        .url-row {{ margin-top: 8px; font-size: 11px; color: #64748b; font-family: monospace; word-break: break-all; }}
        .card-actions {{ display: flex; gap: 8px; border-top: 1px solid #1f2937; padding-top: 12px; }}
        .btn-restart {{
            flex: 1;
            background: #1e293b;
            color: #e2e8f0;
            border: 1px solid #334155;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-restart:hover {{ background: #334155; color: #38bdf8; border-color: #38bdf8; }}
        .btn-ping {{
            background: #1e293b;
            color: #38bdf8;
            border: 1px solid #0369a1;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-ping:hover {{ background: #0284c7; color: white; }}
        .footer {{ max-width: 1100px; margin: 30px auto 0; text-align: center; font-size: 12px; color: #6b7280; }}
        #toast {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: #0284c7;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
            display: none;
            font-size: 13px;
            font-weight: 500;
            z-index: 1000;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">🏥 The Doctor: Swarm Command Center</div>
        <div class="header-controls">
            <span class="quota-badge">🛡️ 750h Free Quota: 100% Protected (1 Node/Acc)</span>
            <span class="badge">Uptime: {uptime_str}</span>
            <span class="badge" id="refreshTimer">Auto-Refresh: 10s</span>
        </div>
    </div>
    
    <div class="toolbar">
        <div>
            <span style="font-size: 13px; color: #94a3b8;">Active Mesh: <b>{len(SERVICES)} Connected Nodes</b> (Zero Dollar Infrastructure)</span>
        </div>
        <div style="display: flex; gap: 8px;">
            <button class="btn-tool" onclick="toggleUrls()">👁️ Toggle URLs</button>
            <button class="btn-primary" onclick="runDiagnostics()">🧪 Run Swarm Diagnostics</button>
        </div>
    </div>
    
    <div class="grid">
        {cards_html}
    </div>
    
    <div class="footer">
        Powered by Render Free Tier (7 Accounts) + FreeLLMAPI + Backblaze B2 | 100% Lifetime Free & Self-Healing Swarm
    </div>
    
    <div id="toast"></div>

    <script>
        let countdown = 10;
        let showFull = false;

        function showToast(msg, bg="#0284c7") {{
            const t = document.getElementById("toast");
            t.innerText = msg;
            t.style.background = bg;
            t.style.display = "block";
            setTimeout(() => {{ t.style.display = "none"; }}, 4000);
        }}

        function toggleUrls() {{
            showFull = !showFull;
            document.querySelectorAll(".masked-url").forEach(el => el.style.display = showFull ? "none" : "inline");
            document.querySelectorAll(".full-url").forEach(el => el.style.display = showFull ? "inline" : "none");
            showToast(showFull ? "Full URLs Visible" : "URLs Masked (Stealth Mode)");
        }}

        async function restartNode(id) {{
            const btn = document.getElementById("btn-" + id);
            const originalText = btn.innerHTML;
            btn.innerHTML = "⏳ Restarting...";
            btn.disabled = true;

            try {{
                const res = await fetch("/api/restart?id=" + encodeURIComponent(id), {{ method: "POST" }});
                const data = await res.json();
                if (data.status === "ok") {{
                    showToast("✓ Restart triggered for " + id, "#10b981");
                    const statusEl = document.getElementById("status-" + id);
                    if (statusEl) {{
                        statusEl.innerText = "RESTARTING";
                        statusEl.style.color = "#f59e0b";
                    }}
                }} else {{
                    showToast("Error: " + data.message, "#ef4444");
                }}
            }} catch (e) {{
                showToast("Request failed: " + e, "#ef4444");
            }} finally {{
                btn.innerHTML = originalText;
                btn.disabled = false;
            }}
        }}

        async function runDiagnostics() {{
            showToast("Running diagnostics pass across all nodes...", "#0284c7");
            try {{
                const res = await fetch("/api/check", {{ method: "POST" }});
                const data = await res.json();
                showToast("✓ Diagnostics Complete! Latencies updated.", "#10b981");
                setTimeout(() => window.location.reload(), 1000);
            }} catch (e) {{
                showToast("Diagnostics error: " + e, "#ef4444");
            }}
        }}

        async function pingNode(id) {{
            showToast("Pinging node " + id + "...", "#0284c7");
            await runDiagnostics();
        }}

        setInterval(() => {{
            countdown--;
            document.getElementById("refreshTimer").innerText = "Auto-Refresh: " + countdown + "s";
            if (countdown <= 0) {{
                countdown = 10;
                window.location.reload();
            }}
        }}, 1000);
    </script>
</body>
</html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def do_HEAD(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path in ("/health", "/ping"):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            return
        if not self.check_auth():
            self.send_response(401)
            self.end_headers()
            return
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # Public endpoints (Keep-alive, uptime monitors, no secret required)
        if path in ("/health", "/ping"):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
            return

        # Protected endpoints
        if not self.check_auth():
            self.render_lock_screen()
            return

        if path in ("/", "/status"):
            self.render_dashboard()
        elif path == "/api/status":
            res = [{
                "id": s["id"],
                "name": s["name"],
                "account": s["account"],
                "status": s["status"],
                "latency_ms": s["latency_ms"],
                "fails": s["consecutive_fails"],
                "restarts": s["restarts"]
            } for s in SERVICES]
            self.send_json(200, res)
        elif path == "/api/check":
            check_services()
            self.send_json(200, {"status": "ok", "message": "Diagnostics completed"})
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        # Public health
        if path in ("/health", "/ping"):
            self.send_response(200)
            self.end_headers()
            return

        # Check auth
        if not self.check_auth():
            self.send_json(401, {"error": "Unauthorized", "message": "Valid admin secret required"})
            return

        if path == "/api/restart":
            svc_id = qs.get("id", [""])[0]
            matched = next((s for s in SERVICES if s["id"] == svc_id), None)
            if not matched:
                self.send_json(404, {"error": "Not Found", "message": f"Service {svc_id} not found"})
                return

            ok, msg = trigger_restart(matched)
            if ok:
                self.send_json(200, {"status": "ok", "message": msg, "restarts": matched["restarts"]})
            else:
                self.send_json(500, {"status": "error", "message": msg})

        elif path in ("/api/check", "/heal"):
            check_services()
            self.send_json(200, {"status": "ok", "message": "Diagnostics pass completed"})
        else:
            self.send_json(404, {"error": "Not Found"})

if __name__ == "__main__":
    t = threading.Thread(target=watchdog_loop, daemon=True)
    t.start()
    server = HTTPServer(("0.0.0.0", PORT), RequestHandler)
    print(f"🏥 The Doctor Sentry running on port {PORT} with Admin Secret protection")
    server.serve_forever()
