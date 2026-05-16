# Simple Flask webhook that downloads an image from session.direct_url and saves it locally.

from flask import Flask, request, jsonify
import datetime
import requests
import os
import uuid
#DB HANDLER 
from db_handler import init_db, save_record, list_records

#DISCORD NOTIFIER
from notify_discord import send_discord_message
init_db()
# A small random id — was used for something
id_random = uuid.uuid4()

# Create the Flask application instance.
app = Flask(__name__)

# Directory where downloaded images will be saved.
DOWNLOAD_DIR = "downloads"
# Ensure the downloads directory exists (no error if it already does).
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Define an endpoint that accepts POST requests at /webhook.
@app.route("/webhook", methods=["POST"])
def webhook():
    # Parse incoming JSON body into a Python dict.
    data = request.get_json()
    
    # Simple console log for debugging: show the parsed payload.
    print("Webhook received:", data)

    # Safely extract the nested "session" object; default to an empty dict if missing.
    session = data.get("session", {})
    event_id = data.get("event_id")

    direct_url = session.get("direct_url")
    device_id_info = session.get("device")
    device_id = device_id_info["name"]
    def get_image_from_direct_url(event_id,direct_url,session_type,device_id):
            if direct_url:
                # Build a timestamp string to use in the filename (YYYYmmdd_HHMMSS).
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                # Note: you can include other identifiers (event id, session id) in the filename if available.
                os.makedirs(f"{DOWNLOAD_DIR}/{event_id}/{session_type}/{device_id}", exist_ok=True)
                filename = os.path.join(f"{DOWNLOAD_DIR}/{event_id}/{session_type}/{device_id}", f"{timestamp}.jpg")

                try:
                    # Perform an HTTP GET to fetch the image bytes.
                    # (consider adding timeout, streaming, and response validation.)
                    img_data = requests.get(direct_url, timeout=10).content

                    # Write the image bytes to the file in binary mode.
                    with open(filename, "wb") as f:
                        f.write(img_data)

                    # Log success with the saved filename.
                    print(f"Image Saved: {filename}")
                    save_record(direct_url, "success")
                    send_discord_message(direct_url, "success", timestamp)
                except Exception as e:
                    # On any failure (network, write permissions, etc.), log the error.
                    # (Consider more specific exception handling and returning an error response.)
                    print(f"Download Failed: {e}")
                    save_record(direct_url, "failed")
                    send_discord_message(direct_url, "success", timestamp)
            else:
                    print("No direct_url in payload - nothing to save.")
    # From the session, get the "direct_url" field (expected to be an image URL).


    session_type = session.get("type")
    if session_type:
        if session_type in "gif":
            get_image_from_direct_url(event_id,direct_url,session_type,device_id)


    # Always return a simple JSON response and HTTP 200 to acknowledge the webhook.
    return jsonify({"status": "ok"}), 200


# Run the app when executed directly. Defaults to port 5000.
if __name__ == "__main__":
    app.run(port=5000)
    print(f"RESULTS:\n")
    print(f"\n".join(list_records(5)))