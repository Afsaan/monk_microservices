FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY app /app

EXPOSE 72

ENV UVICORN_CMD="uvicorn app/main:app --host 0.0.0.0 --port 72"

CMD ["sh", "-c", "$UVICORN_CMD"]