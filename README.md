This is the backend service for the CodeAnalysis project, built with Django and Django REST Framework.

## Features

- RESTful API for code analysis and interview preparation
- User authentication (JWT)
- AI/LLM integration (Dolphin 3.0 via OpenRouter API)
- Caching with Redis
- Rate limiting with `django-ratelimit`
- WebSocket support for real-time features

## Tech Stack

- Python 3.9+
- Django
- Django REST Framework
- Redis (for caching)
- SQLite (development) / PostgreSQL (production)
- Gunicorn (for production WSGI serving)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/CodeAnalysis.git
cd CodeAnalysis/CodeAnalysisBackend
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and update the values as needed (API keys, database, etc).

### 5. Run database migrations

```bash
python manage.py migrate
```

### 6. (Optional) Start Redis server

If using Redis locally for caching/rate limiting:

```bash
redis-server
```

### 7. Run the development server

```bash
python manage.py runserver
```

## Deployment

- For production, use Gunicorn or another WSGI server.
- See `Dockerfile` for containerization.
- Example (after building Docker image):

```bash
gunicorn CodeAnalysis.wsgi:application --bind 0.0.0.0:8000
```

## Environment Variables

- `OPENROUTER_API_KEY` - Your OpenRouter API key for AI features
- `DATABASE_URL` - Database connection string (default: SQLite)
- `REDIS_URL` - Redis connection string (default: redis://localhost:6379/0)
- `DJANGO_SECRET_KEY` - Django secret key
- `ALLOWED_HOSTS` - Allowed hosts for Django

## License

MIT

---

For more details, see the main [README.md](../README.md).
