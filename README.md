Project: webhook-server (in development)

Short description

    Simple Flask webhook that receives JSON payloads, downloads media from session.direct_url, saves files locally, records events in SQLite, and notifies a Discord webhook.

Prerequisites

    Python 3.10+ (recommended)
    Git
    Tailscale (optional — used in run_server.sh)
    A Discord webhook URL (set in .env as DISCORD_WEBHOOK_URL)

Quick setup

    Clone repository and change into the project folder.

    Create a virtual environment and install dependencies:
        python -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt

    Create a .env file in the project root with, your Discord Webhook:
        DISCORD_WEBHOOK_URL="your URL here"

    Start the server locally:
        source .venv/bin/activate
        python webhook_server.py
        Server listens on port 5000 by default.
    You can either funnel it yourself or use tailscale

Run with run_server.sh (optional *requires an active tailscale connection)

    Make script executable: chmod +x run_server.sh
    Usage:
        ./run_server.sh start
        ./run_server.sh stop
        ./run_server.sh restart
        ./run_server.sh status
    Notes:
        start uses .venv/bin/python and may run tailscale up + tailscale funnel 5000.
        Adjust or remove tailscale calls if not needed.
        This repo is meant as a small personal tool, so the shell helper is optional, and use is "HERE BE DRAGONS" so if something breaks, kid that's on you

What the main files do

    webhook_server.py
        Flask app with POST /webhook endpoint.
        Downloads media from session.direct_url and saves it under downloads/{event_id}/{session_type}/{device_id}/.
        Records each attempt in SQLite via db_handler.
        Sends a Discord notification via notify_discord.
    db_handler.py
        Initializes SQLite DB at db/webhook_data.db.
        Functions: init_db(), save_record(direct_url, status), list_records(LIMIT=10).
    notify_discord.py
        Sends a Discord content payload to DISCORD_WEBHOOK_URL using requests.
    logsaint.py
        Optional Discord status notifier for server lifecycle and results.
    requirements.txt
        Fixed package versions used in development.
    run_server.sh
        Optional helper to start/stop the Flask app and manage Tailscale funnel.

Known issues & TODO (in-development)

    - Input validation is weak; missing event_id/session/direct_url may cause errors or be ignored.
    - Error handling is broad and the webhook always returns HTTP 200.
    - File downloads are saved without streaming or URL validation.
    - Logging uses print() instead of a proper logging framework.
    - Filenames use timestamps only, so collisions are possible for repeated events.
    - logsaint.py uses incorrect membership checks for status values.
    - notify_discord.py currently assumes event_id may be numeric when checking int(event_id) == 1.

Bug summary

    webhook_server.py:
        - event_id and direct_url defaults should not use {}.
        - device_id extraction is fragile if session or device.name is missing.
        - session_type checks should use equality instead of membership in a string.
        - error handling currently sends success notifications even on failure.
        - missing direct_url still returns 200.
    db_handler.py:
        - current list_records formatting is correct for the selected columns.
    notify_discord.py:
        - content generation is duplicated and could be simplified.
        - int(event_id) == 1 may crash for non-numeric event IDs.

Recommended quick fixes

    - Use safe lookups for nested session fields.
    - Validate required payload fields and return 400 for invalid input.
    - Send failure status on download exceptions.
    - Use explicit session_type comparisons.
    - Add UUID or unique suffix to filenames to avoid collisions.
    - Switch from print() to Python logging when ready.

Example sample payload

    POST /webhook JSON: { "event_id": "evt_12345", "session": { "direct_url": "https://example.com/path/image.jpg", "type": "still", "device": { "name": "cam1" } } }

Database schema

    downloads (id INTEGER PK AUTOINCREMENT, timestamp TEXT, direct_url TEXT, status TEXT)

Development tips

    - Run the app locally and send test payloads with curl or Postman.
    - Keep this repo as lightweight personal tooling rather than production-grade deployment.
    - Use ngrok or Tailscale funnel only if you need external exposure.
 