FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10
LABEL authors="fff"

RUN apt-get update && \
    apt-get install -y \
    tesseract-ocr-rus \
    poppler-utils

COPY ./text_extractor /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 80