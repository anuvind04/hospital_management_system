FROM python:3.14.3-slim

WORKDIR /app

COPY hms/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY hms/ .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && exec gunicorn hms.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]