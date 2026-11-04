# Україна починається з тебе

Django-сайт з рекордсменами по областях України.

## Локально
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Деплой (гілка `develop`)
Змінні оточення: див. `.env.example` (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`).
Опційно: `DJANGO_DB_PATH`, `DJANGO_MEDIA_ROOT` (шляхи на постійному диску).

- **Docker:** `docker build -t ukraine . && docker run -p 8000:8000 --env-file .env ukraine`
- **Heroku/Render-стиль:** `Procfile` (release: migrate, web: gunicorn).
- Статика віддається через WhiteNoise, медіа — через Django (`/media/`).
- CI: `.github/workflows/deploy.yml` запускається на push у `develop`.
