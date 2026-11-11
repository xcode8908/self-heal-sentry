import os
import time
import json
import urllib.request
import urllib.error
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 10000))

SERVICES = [
    {
        "id": "nanobot-master",
        "name": "Nanobot Master (Chief AI)",
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
        "url": os.environ.get("URL_FREELLM", "https://freellm.silentxop.workers.dev/v1/models"),
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
        "name": "Worker 5: Automator & Workflow Engine",
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
        "id": "picoclaw-worker-6",
        "name": "Worker 6: Generalist PicoClaw Assistant",
        "url": os.environ.get("URL_WORKER6", "https://picoclaw-0c71.onrender.com/health"),
        "srv_id": os.environ.get("SRV_WORKER6", "srv-dalojee1egvs73fb6gt0"),
        "token": os.environ.get("TOK_WORKER6", "rnd_kN4R27A9gB7xkt9Rf6ioMftEVNBY"),
        "consecutive_fails": 0,
        "status": "starting",
        "latency_ms": 0,
        "last_checked": 0,
        "restarts": 0
    }
]

START_TIME = time.time()
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8888310796:AAE8vPg6DC-RcSxZb1YKYm_EiIxwtCjObAM")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "8888310796")

def send_telegram_alert(msg: str):
    if not TELEGRAM_BOT_TOKEN:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"[Alert Error] {e}")

def trigger_heal(s):
    if not s["srv_id"] or not s["token"]:
        print(f"[Doctor] Cannot heal {s['name']} (missing srv_id or token)")
        return
    print(f"🚨 [Doctor] Triggering auto-redeploy for {s['name']} ({s['srv_id']})...")
    url = f"https://api.render.com/v1/services/{s['srv_id']}/deploys"
    payload = json.dumps({"clearCache": "do_not_clear"}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Authorization": f"Bearer {s['token']}", "Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            dep_id = data.get("id", "unknown")
            s["restarts"] += 1
            s["consecutive_fails"] = 0
            alert_msg = f"🏥 *The Doctor Self-Heal Alert*\n\n⚡ *Node:* `{s['name']}` was non-responsive.\n🔄 *Action:* Auto-redeploy triggered on Render (`{dep_id}`).\n🕒 Restarts count: {s['restarts']}"
            send_telegram_alert(alert_msg)
            print(f"✓ Successfully triggered redeploy {dep_id} for {s['name']}")
    except Exception as e:
        print(f"Error triggering redeploy: {e}")

def check_services():
    for s in SERVICES:
        t0 = time.time()
        headers = {"User-Agent": "Mozilla/5.0"}
        if "freellm" in s["id"]:
            headers["Authorization"] = "Bearer freellmapi-4737972ff9f51574683ace9510d73dc179fc3ee310fcd250"
        try:
            req = urllib.request.Request(s["url"], headers=headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                status_code = resp.status
                latency = round((time.time() - t0) * 1000, 1)
                s["latency_ms"] = latency
                s["last_checked"] = time.time()
                if 200 <= status_code < 400:
                    s["status"] = "healthy"
                    s["consecutive_fails"] = 0
                else:
                    s["status"] = f"unhealthy ({status_code})"
                    s["consecutive_fails"] += 1
        except Exception as e:
            latency = round((time.time() - t0) * 1000, 1)
            s["latency_ms"] = latency
            s["last_checked"] = time.time()
            s["status"] = "offline"
            s["consecutive_fails"] += 1
            print(f"[Watchdog] Check failed for {s['name']}: {e}")

        if s["consecutive_fails"] >= 3:
            trigger_heal(s)

def watchdog_loop():
    print("[Doctor] Watchdog thread started. Monitoring all 8 swarm nodes every 30s...")
    while True:
        try:
            check_services()
        except Exception as e:
            print(f"[Doctor Loop Error] {e}")
        time.sleep(30)

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            uptime = int(time.time() - START_TIME)
            all_healthy = all(s["status"] == "healthy" for s in SERVICES)
            res = {
                "status": "healthy" if all_healthy else "degraded",
                "role": "Self-Heal Sentry (The Doctor)",
                "uptime_seconds": uptime,
                "monitored_nodes_count": len(SERVICES),
                "nodes": [
                    {
                        "id": s["id"],
                        "name": s["name"],
                        "status": s["status"],
                        "latency_ms": s["latency_ms"],
                        "consecutive_fails": s["consecutive_fails"],
                        "restarts": s["restarts"]
                    }
                    for s in SERVICES
                ]
            }
            self.wfile.write(json.dumps(res, indent=2).encode("utf-8"))
        elif self.path == "/ping":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"pong")
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            uptime = int(time.time() - START_TIME)
            
            rows = ""
            for s in SERVICES:
                badge_color = "#10b981" if s["status"] == "healthy" else ("#f59e0b" if "starting" in s["status"] else "#ef4444")
                rows += f"""
                <div class="card">
                    <div class="card-header">
                        <span class="dot" style="background: {badge_color};"></span>
                        <span class="card-title">{s['name']}</span>
                    </div>
                    <div class="card-meta">
                        <div><b>Status:</b> <span style="color: {badge_color};">{s['status'].upper()}</span></div>
                        <div><b>Latency:</b> {s['latency_ms']} ms</div>
                        <div><b>Consecutive Fails:</b> {s['consecutive_fails']}/3</div>
                        <div><b>Auto-Restarts:</b> {s['restarts']}</div>
                        <div class="url"><a href="{s['url']}" target="_blank">{s['url']}</a></div>
                    </div>
                </div>
                """
                
            html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏥 The Doctor - Multi-Agent Swarm Sentry</title>
    <meta http-equiv="refresh" content="10">
    <style>
        body {{
            background: #090d16;
            color: #f3f4f6;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 24px;
        }}
        .header {{
            max-width: 1000px;
            margin: 0 auto 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #1f2937;
            padding-bottom: 16px;
        }}
        .title {{ font-size: 24px; font-weight: 700; color: #38bdf8; display: flex; align-items: center; gap: 10px; }}
        .badge {{ background: #1e293b; padding: 6px 14px; border-radius: 9999px; font-size: 13px; color: #94a3b8; border: 1px solid #334155; }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 16px;
            max-width: 1000px;
            margin: 0 auto;
        }}
        .card {{
            background: #111827;
            border: 1px solid #1f2937;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s, border-color 0.2s;
        }}
        .card:hover {{ border-color: #38bdf8; transform: translateY(-2px); }}
        .card-header {{ display: flex; align-items: center; gap: 10px; margin-bottom: 12px; font-weight: 600; font-size: 15px; }}
        .dot {{ width: 10px; height: 10px; border-radius: 50%; box-shadow: 0 0 8px currentColor; }}
        .card-meta {{ font-size: 13px; color: #9ca3af; line-height: 1.8; }}
        .url {{ margin-top: 8px; font-size: 11px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .url a {{ color: #38bdf8; text-decoration: none; }}
        .footer {{ max-width: 1000px; margin: 30px auto 0; text-align: center; font-size: 12px; color: #6b7280; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">🏥 The Doctor: Self-Heal Sentry</div>
        <div class="badge">Uptime: {uptime}s | Auto-Refresh: 10s</div>
    </div>
    <div class="grid">
        {rows}
    </div>
    <div class="footer">
        Powered by Render Free Tier (7 Nodes) + FreeLLMAPI + Backblaze B2 | 100% Lifetime Free & Self-Healing
    </div>
</body>
</html>
"""
            self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        if self.path == "/heal":
            check_services()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "heal pass completed"}')
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    t = threading.Thread(target=watchdog_loop, daemon=True)
    t.start()
    server = HTTPServer(("0.0.0.0", PORT), RequestHandler)
    print(f"🏥 The Doctor server running on port {PORT}")
    server.serve_forever()
