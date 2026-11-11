# 🏥 The Doctor - Self-Heal Sentry

High-availability autonomous watchdog and self-healing sentry for the Nanobot + 6 PicoClaw Multi-Agent Swarm.

### Capabilities:
- Pings all 8 agents every 30 seconds (Keep-Alive mechanism).
- Auto-detects degraded or crashed services.
- Auto-restarts / redeploys failing services via Render API after 3 consecutive failed checks.
- Dispatches instant alerts to Telegram.
- Serves `/health` for Uptime Kuma monitoring and `/` with live cyberpunk visual dashboard.
