#!/bin/sh

# Apply database migrations
echo "Apply database migrations"
python3 manage.py makemigrations
python3 manage.py migrate

echo "Run unit tests"
python3 manage.py test task_backend.users.tests.test_model_users task_backend.users.tests.test_api_users task_backend.projects.tests.test_model_projects task_backend.projects.tests.test_api_projects --verbosity=2 --parallel

# Start server
echo "--> Starting web process"
gunicorn config.wsgi:application -b 0.0.0.0:8000