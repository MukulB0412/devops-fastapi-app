FROM python:3.11-slim

WORKDIR /app
COPY app/ /app
COPY app/requirements.txt .

RUN pip install -r requirements.txt

ENV PORT=8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
