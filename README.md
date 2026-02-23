# notification-microservice

Notification microservice for task/activity updates (User Story 1: notify on task completion). In-app channel only; email (Mailgun) added in User Story 2.

## Run locally

1. Create a virtualenv and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # or `venv\Scripts\activate` on Windows
   python3 -m pip install -r requirements.txt
   ```

2. Start the server:
   ```bash
   python3 app.py
   ```
   Server listens on `http://0.0.0.0:3000` (set `PORT` to override).

## API

### POST /api/send

Send a notification when a task/activity is completed.

**Request body (JSON):**

| Field              | Required | Description                               |
|--------------------|----------|-------------------------------------------|
| `user_id`          | Yes      | ID of the user to notify                  |
| `activity_id`      | Yes      | ID of the task or activity                |
| `notification_type` | Yes    | e.g. `activity_completed`                 |
| `channel`          | No       | Preferred channel(s); US1: `["in-app"]`   |

**Example:**
```bash
curl -X POST http://localhost:3000/api/send \
  -H "Content-Type: application/json" \
  -d '{"user_id": 123, "activity_id": 456, "notification_type": "activity_completed", "channel": ["in-app"]}'
```

**Response (JSON):**
```json
{
  "status": "success",
  "user_id": "123",
  "activity_id": "456",
  "notification_type": "activity_completed",
  "timestamp": "2026-02-23T12:00:00Z",
  "error_message": null
}
```
On failure, `status` is `"failure"` and `error_message` contains the reason.

### GET /health

Health check; returns `{"status": "ok"}`.

---

## Teammate: Where to plug in (Preferences)

User notification preferences are currently provided by a **stub** (all channels enabled for everyone). To persist and respect real preferences, implement `preferences/impl.py`: `get_enabled_channels(user_id: str) -> list[str]`. See `preferences/impl.py` and `send/orchestrator.py` for the contract.
