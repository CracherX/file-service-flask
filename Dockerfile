FROM python:3.12.3-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    locales && \
    rm -rf /var/lib/apt/lists/*

RUN sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=ru_RU.UTF-8

ENV LANG=ru_RU.UTF-8 \
    LANGUAGE=ru_RU:ru \
    LC_ALL=ru_RU.UTF-8 \
    PYTHONIOENCODING=utf-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80
WORKDIR /app/src

CMD ["uwsgi", "--ini", "../uwsgi.ini"]