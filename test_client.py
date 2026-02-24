#!/usr/bin/env python3
# Hits the notification service over HTTP. Run the server first (python3 app.py).

import os
import requests

BASE_URL = os.environ.get("NOTIFICATION_SERVICE_URL", "http://localhost:3000")


def request_send_notification(user_id, activity_id, notification_type, channel=None, email=None):
    """POST /api/send, returns JSON."""
    url = f"{BASE_URL}/api/send"
    payload = {
        "user_id": user_id,
        "activity_id": activity_id,
        "notification_type": notification_type,
    }
    if channel is not None:
        payload["channel"] = channel if isinstance(channel, list) else [channel]
    if email is not None:
        payload["email"] = email
    resp = requests.post(url, json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()


def request_user_preferences(user_id):
    """GET user prefs, returns JSON."""
    url = f"{BASE_URL}/users/{user_id}/preferences"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()


def request_health():
    """GET /health, returns JSON."""
    url = f"{BASE_URL}/health"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()


def main():
    print("Test client for notification microservice.\n")

    # health
    print("1. Health check...")
    health_data = request_health()
    print(f"   Got: {health_data}\n")

    # prefs
    print("2. User preferences (user_id=1)...")
    prefs_data = request_user_preferences("1")
    print(f"   Got: {prefs_data}\n")

    # send
    print("3. Send notification...")
    send_data = request_send_notification(
        user_id=123,
        activity_id=456,
        notification_type="activity_completed",
        channel=["in-app"],
    )
    print(f"   Got: {send_data}\n")

    print("Done.")


if __name__ == "__main__":
    main()
