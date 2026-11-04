release: python manage.py migrate --noinput
web: gunicorn project.wsgi --bind 0.0.0.0:${PORT:-8000} --workers 2
