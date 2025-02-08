FROM python:3.9-alpine

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD [ "gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]

