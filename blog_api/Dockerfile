FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

Run pip install -r requirements.txt

COPY app /app

EXPOSE 8000

ENV UVICORN_CMD="uvicorn main:app --host 0.0.0.0 --port 8000"

CMD ["sh", "-c", "$UVICORN_CMD"]