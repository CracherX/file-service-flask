FROM python:3.12.3-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && pip install --upgrade pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80
WORKDIR /app/src

CMD  uwsgi --ini ../uwsgi.ini