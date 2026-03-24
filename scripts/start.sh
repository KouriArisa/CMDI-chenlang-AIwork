#!/usr/bin/env sh
set -eu

: "${DJANGO_SETTINGS_MODULE:=config.settings.local}"
: "${DJANGO_DEBUG:=False}"
: "${PORT:=8000}"
: "${GUNICORN_WORKERS:=3}"
: "${GUNICORN_TIMEOUT:=60}"
: "${DB_WAIT_MAX_ATTEMPTS:=20}"
: "${DB_WAIT_INTERVAL:=3}"

required_vars="DJANGO_SECRET_KEY DJANGO_ALLOWED_HOSTS MYSQL_DATABASE MYSQL_USER MYSQL_PASSWORD MYSQL_HOST MYSQL_PORT"

for var_name in $required_vars; do
  eval "var_value=\${$var_name:-}"
  if [ -z "$var_value" ]; then
    echo "Missing required environment variable: $var_name" >&2
    exit 1
  fi
done

if [ "$MYSQL_PASSWORD" = "change-this-password" ]; then
  echo "MYSQL_PASSWORD is still set to the example placeholder." >&2
  exit 1
fi

echo "Starting Django with DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}, PORT=${PORT}, DEBUG=${DJANGO_DEBUG}"
echo "Waiting for database ${MYSQL_HOST}:${MYSQL_PORT}..."

python - <<'PY'
import os
import sys
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE", "config.settings.local"))

from django.db import connections
from django.db.utils import OperationalError

max_attempts = int(os.getenv("DB_WAIT_MAX_ATTEMPTS", "20"))
wait_interval = int(os.getenv("DB_WAIT_INTERVAL", "3"))

for attempt in range(1, max_attempts + 1):
    try:
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        print("Database connection ready.")
        sys.exit(0)
    except OperationalError as exc:
        print(f"[{attempt}/{max_attempts}] Database not ready: {exc}")
        time.sleep(wait_interval)

print("Database connection timed out.", file=sys.stderr)
sys.exit(1)
PY

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn config.wsgi:application \
  --bind "0.0.0.0:${PORT}" \
  --workers "${GUNICORN_WORKERS}" \
  --timeout "${GUNICORN_TIMEOUT}"
