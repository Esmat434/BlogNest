set -o errexit

python -m pip install --upgrade pip

pip install -r requirements.txt

python manage.py migrate

if [[$CREATE_SUPERUSER]];
then
    python manage.py createsuperuser --no-input --email "$DJANGO_SUPERUSER_EMAIL"
fi