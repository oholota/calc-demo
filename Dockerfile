# The whole runtime in one file: OS, Python, libraries, app, start command.
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /srv

# Dependencies first: this layer is rebuilt only when requirements.txt changes.
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/
WORKDIR /srv/app
RUN python manage.py collectstatic --noinput

# Do not run as root. A numeric UID lets Kubernetes verify runAsNonRoot.
RUN useradd --uid 10001 --create-home app
USER 10001

# Production settings. "*" keeps the demo simple; a real service lists its hostnames.
ENV DJANGO_DEBUG=0 \
    DJANGO_ALLOWED_HOSTS="*" \
    PORT=8000
EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:%s/healthz' % os.environ.get('PORT', '8000'), timeout=2)"

# gunicorn instead of "manage.py runserver": runserver is a development server.
CMD ["sh", "-c", "exec gunicorn calcsite.wsgi:application --bind 0.0.0.0:${PORT} --workers 2 --access-logfile -"]
