Project: webhook-server (in development)

Short description

    Flask webhook that receives JSON payloads, downloads media from session.direct_url, saves files locally, records events in SQLite, and notifies a Discord webhook.

Prerequisites

    Python 3.10+ (recommended)
    Git
    Tailscale (optional — used in run_server.sh)
    A Discord webhook URL (set in .env as DISCORD_WEBHOOK_URL)

Quick setup

    Clone repository:
        git clone && cd

    Create virtual environment and install dependencies:
        python -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt

    Create .env file in project root with:
        DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."

    Start the server (development):
        source .venv/bin/activate
        python webhook_server.py
        Server listens on port 5000 by default.

Run with run_server.sh (optional)

    Make script executable: chmod +x run_server.sh
    Usage:
        ./run_server.sh start
        ./run_server.sh stop
        ./run_server.sh restart
        ./run_server.sh status
    Notes:
        start uses .venv/bin/python and runs tailscale up + tailscale funnel 5000 (requires sudo).
        Adjust or remove tailscale calls if not needed.

What the main files do

    webhook_server.py
        Flask app with POST /webhook endpoint.
        Downloads media from session.direct_url and saves it under downloads/{event_id}/{session_type}/{device_id}/.
        Records each attempt in SQLite via db_handler and sends a Discord notification via notify_discord.
    db_handler.py
        Initializes SQLite DB at db/webhook_data.db.
        Functions: init_db(), save_record(direct_url, status), list_records(LIMIT=10).
    notify_discord.py
        Sends a simple message payload to DISCORD_WEBHOOK_URL using requests.
    requirements.txt
        Exact package versions used in development.
    run_server.sh
        Helper to run the Flask app in background and manage Tailscale funnel process.

Known issues & TODO (in-development)

    Input validation: payload parsing uses dict.get in places but some assignments are incorrect (see bugs below).
    Error handling: network and file errors are broadly caught; return status codes currently always 200.
    Concurrency: SQLite connections are created per call; consider connection pooling for high throughput.
    File naming / collisions: filenames use timestamps only — consider adding uuid to avoid collisions for fast repeated events.
    Security: direct_url is requested without validation; consider validating domain/headers and using streaming requests.
    Discord notify: on exception, the notify path prints errors but does not affect response.
    Logging: use Python logging instead of print for better level control and persistence.
    Tests: add unit tests and integration tests for webhook handling, DB writes, and notify logic.

Bug summary (things to fix before production)

    db_handler.list_records builds strings using wrong tuple order (f"[{ts}] {status.upper()} -> {url}" for ts, url, status) — order mismatch.
    webhook_server.py:
        event_id, direct_url, and device_id extraction use {} as defaults and build device_id incorrectly:
            event_id = data.get("event_id",{}) should default to None or "" and treated as string.
            direct_url = session.get("direct_url",{}) should default to None.
            device handling sets device_id = device_id_info["name"],{} which produces a tuple; should be device_id_info.get("name", "unknown").
        get_from_direct_url: session_type checks use if session_type in "video": which checks characters, not equality; should use == or in a list.
        get_from_direct_url uses send_discord_message(..., "success", timestamp) in except block (should send "failed").
        When direct_url is falsy, code prints fallback but still returns 200; consider returning 400 for missing required fields.
        Filenames only use timestamp and not unique identifiers — collisions possible.
    notify_discord.py content string missing colon/space before URL ("URL{direct_url}").

Recommended quick fixes

    Fix device_id extraction:
        device_id = session.get("device", {}).get("name", "unknown")
    Use equality checks for session_type:
        if session_type == "video": ...
    Correct error notify call to use "failed" status in except.
    Fix db_handler.list_records tuple unpacking order.
    Validate direct_url and event_id presence; return 400 if missing.
    Improve filename uniqueness: use f"{timestamp}{uuid.uuid4().hex[:8]}.ext
    Add timeouts and streaming to requests.get (stream=True) and check response.status_code.
    Replace print() with logging and rotate logs_

Example sample payload

    POST /webhook JSON: { "event_id": "evt_12345", "session": { "direct_url": "https://example.com/path/image.jpg", "type": "still", "device": { "name": "cam1" } } }

Database schema

    downloads (id INTEGER PK AUTOINCREMENT, timestamp TEXT, direct_url TEXT, status TEXT_

Development tips

    Run the app locally and send test payloads with curl or Postman.
    Inspect webhook_server.log and funnel.log when using run_server.sh.
    Use ngrok or Tailscale funnel only if you need external access; 