"""
LexGuard AI — WSGI Entry Point
Use this file with a production WSGI server, e.g.:

  gunicorn wsgi:application --workers 4 --bind 0.0.0.0:8000
"""
from app import create_app

application = create_app("production")

if __name__ == "__main__":
    application.run()
