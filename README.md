# Access Control Log API

A simple Django REST API for logging door access events.  
This project was built as a technical task simulating a small part of an access control ecosystem.

---

## Tech Stack
- Python
- Django
- Django REST Framework
- SQLite (default database)
- django-filter
- Docker (bonus)

---

## Data Model

### AccessLog
Represents a single door access attempt.

| Field | Description |
|------|------------|
| card_id | Identifier of a physical access card (e.g. `C1001`). The same card may appear in multiple log entries. |
| door_name | Name of the accessed door |
| access_granted | Whether access was granted (`true`) or denied (`false`) |
| timestamp | Automatically recorded creation time |

> Note: “unique card identifier” refers to the physical card itself, not a database-level uniqueness constraint on log entries.

---

## API Endpoints

Base URL: `/api`

| Method | Endpoint | Description |
|------|---------|-------------|
| POST | `/api/logs/` | Create a new access log |
| GET | `/api/logs/` | List all access logs |
| GET | `/api/logs/<id>/` | Retrieve a single access log |
| PUT | `/api/logs/<id>/` | Update an access log (timestamp is read-only) |
| DELETE | `/api/logs/<id>/` | Delete an access log (returns 204) |

### Filtering
Logs can be filtered by card ID:

```
GET /api/logs/?card_id=C1001
```

---

## System Event Logging

Django signals are used to log system events to an external file:

- **Create** (`post_save`): logs a CREATE event
- **Delete** (`post_delete`): logs a DELETE event
- Logging is performed using Python’s `subprocess` module
- Events are appended to `system_events.log` in the project root

---

## Local Setup

### 1. Create and activate virtual environment
```bash
python -m venv .venv
```

Windows:
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run migrations
```bash
python manage.py migrate
```

### 4. Start development server
```bash
python manage.py runserver
```

API available at:
```
http://127.0.0.1:8000/api/logs/
```

---

## Running Tests
```bash
python manage.py test
```

---

## Docker (Bonus)

### Build image
```bash
docker build -t access-control-log-api .
```

### Run container
```bash
docker run --rm -p 8000:8000 access-control-log-api
```

The container runs migrations automatically on startup.

---

## Notes
- `.env` is ignored by Git; `.env.example` is provided for reference
- SQLite database is used for simplicity
- The development server is used for demonstration purposes
