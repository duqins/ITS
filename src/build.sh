#!/usr/bin/env bash
# Render runs this on every deploy (render.yaml). seed_demo only adds data to an empty database.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
# Neon advises its direct address for creating tables; the app itself uses the pooled DATABASE_URL.
DATABASE_URL="${DATABASE_URL_UNPOOLED:-$DATABASE_URL}" python manage.py migrate --no-input
DATABASE_URL="${DATABASE_URL_UNPOOLED:-$DATABASE_URL}" python manage.py seed_demo
