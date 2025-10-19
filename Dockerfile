FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY config/.env.example /app/config/.env.example

EXPOSE 8088

CMD ["uvicorn", "app.rag_api.main:app", "--host", "0.0.0.0", "--port", "8088"]
