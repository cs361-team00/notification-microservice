# POST /api/send for task-completion notifications
from dotenv import load_dotenv
load_dotenv()

import logging
from flask import Flask, request, jsonify

from send.orchestrator import send_notification

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/api/send", methods=["POST"])
def api_send():
    try:
        data = request.get_json(force=True, silent=True) or {}
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400

    user_id = data.get("user_id")
    activity_id = data.get("activity_id")
    notification_type = data.get("notification_type")
    channel = data.get("channel")
    email = data.get("email")

    if user_id is None or activity_id is None or notification_type is None:
        return jsonify({
            "error": "Missing required fields: user_id, activity_id, notification_type",
        }), 400

    # allow channel as single string or list
    if channel is not None and not isinstance(channel, list):
        channel = [channel] if isinstance(channel, str) else None
    if channel is not None:
        channel = [str(c) for c in channel]

    result = send_notification(
        user_id=str(user_id),
        activity_id=str(activity_id),
        notification_type=str(notification_type),
        channel_hint=channel,
        to_email=str(email).strip() if email else None,
    )
    return jsonify(result), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=False)
