## 📘 `README.md`

````markdown
# alx-backend-security

A Django-based backend security project implementing IP tracking, blacklisting, geolocation analytics, rate limiting, and anomaly detection.

## 🚀 Features

### ✅ Task 0: Basic IP Logging Middleware
- Logs each incoming request's:
  - IP address
  - Timestamp
  - Request path

### ✅ Task 1: IP Blacklisting
- Blocks requests from blacklisted IPs (403 Forbidden)
- IPs can be added via a custom management command:
  ```bash
  python manage.py block_ip <ip_address>
````

### ✅ Task 2: IP Geolocation Analytics

* Logs country and city info for each IP
* Uses external geolocation API (e.g., `ipapi.co`)
* Results are cached for 24 hours to reduce API calls

### ✅ Task 3: Rate Limiting by IP

* Rate limits based on IP address using `django-ratelimit`
* Limits:

  * 10 requests/min for authenticated users
  * 5 requests/min for anonymous users
* Returns `429 Too Many Requests` if exceeded

### ✅ Task 4: Anomaly Detection

* Celery task to run hourly:

  * Flags IPs with >100 requests/hour
  * Flags IPs accessing sensitive paths (`/admin`, `/login`)
* Flagged IPs are stored in `SuspiciousIP` model

---

## 🧰 Requirements

* Python 3.8+
* Django 4+
* Redis (for Celery and caching)
* Dependencies (see below)

### 🔌 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🏁 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/alx-backend-security.git
cd alx-backend-security
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6. Run the Server

```bash
python manage.py runserver
```

---

## 🌐 Testing

### IP Logging

Visit any route, then check logs:

```bash
python manage.py shell
>>> from ip_tracking.models import RequestLog
>>> RequestLog.objects.all()
```

### IP Blacklisting

```bash
python manage.py block_ip 127.0.0.1
```

Reload the site to receive a 403 error.

### Rate Limiting

Access `/anon-test/` or `/auth-test/` more than the allowed times per minute to receive a 429 error.

### Anomaly Detection

Simulate requests and run:

```bash
python manage.py shell
>>> from ip_tracking.tasks import detect_anomalies
>>> detect_anomalies()
```

---

## ⚙️ Celery Setup (Optional for Task 4)

Start a Redis server:

```bash
redis-server
```

Start Celery worker:

```bash
celery -A alx_backend_security worker --loglevel=info
```

(Optional) Add periodic tasks with Celery Beat.

---

## 📂 Project Structure

```
alx-backend-security/
├── ip_tracking/
│   ├── middleware.py
│   ├── models.py
│   ├── views.py
│   ├── tasks.py
│   └── management/
│       └── commands/
│           └── block_ip.py
├── alx_backend_security/
│   └── settings.py
├── manage.py
└── README.md
```

---

## 📦 Sample `requirements.txt`

```txt
Django>=4.0
django-ratelimit
requests
celery
redis
```

---

## 📜 License

This project is part of the ALX Software Engineering curriculum. All rights reserved by the authors and ALX program.

```

---

