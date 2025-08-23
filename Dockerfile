FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# deps สำหรับ psycopg3 และ OpenCV (ถ้าโปรเจ็กต์คุณ import cv2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev pkg-config \
    libgl1 libglib2.0-0 libsm6 libxext6 libxrender1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

EXPOSE 8000
