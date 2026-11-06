FROM python:3.14.3-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY hms/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY hms/ .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
