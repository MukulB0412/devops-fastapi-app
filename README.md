# FastAPI + PostgreSQL App on AWS EKS (Kubernetes)

This project demonstrates how to build a containerized FastAPI application that connects to a PostgreSQL database and deploy it on AWS EKS using Kubernetes.

---

## 🧑‍💻 Tech Stack
- **FastAPI**
- **PostgreSQL**
- **Docker**
- **GitHub Actions**
- **Kubernetes**
- **AWS EKS**

---

## 📁 Project Structure

```
.
├── main.py
├── requirements.txt
├── Dockerfile
├── .github/workflows/docker-image.yml
├── deployment.yml
└── service.yml
```

---

## 🚀 FastAPI Code (`main.py`)

```python
from fastapi import FastAPI
import os
import psycopg2

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "FastAPI working inside Docker!"}

@app.get("/db")
def db_check():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            dbname=os.getenv("DB_NAME")
        )
        return {"status": "Connected to PostgreSQL"}
    except:
        return {"status": "DB Connection Failed"}
```

---

## 📦 Requirements (`requirements.txt`)

```
fastapi
uvicorn
psycopg2-binary
```

---

## 🐳 Dockerfile

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV HOST=0.0.0.0
ENV PORT=8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🔄 GitHub Actions Workflow (`.github/workflows/docker-image.yml`)

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

    - name: Log in to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build and Push Docker image
      run: |
        docker build -t mukul0412/fastapi-k8s-app:latest .
        docker push mukul0412/fastapi-k8s-app:latest
```

---

## ☸ Kubernetes Deployment (`deployment.yml`)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
      - name: fastapi-container
        image: mukul0412/fastapi-k8s-app:latest
        ports:
        - containerPort: 8000
```

---

## ☸ Kubernetes Service (`service.yml`)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  type: LoadBalancer
  selector:
    app: fastapi
  ports:
    - port: 80
      targetPort: 8000
```

---

## 🧾 Steps Followed

1. Created FastAPI app (`main.py`)
2. Added requirements and Dockerized the app
3. Built and pushed image to Docker Hub using GitHub Actions
4. Created `deployment.yml` and `service.yml` for Kubernetes
5. Created EKS cluster via AWS Console (GUI) under Free Tier
6. Configured kubectl with:
   ```
   aws eks update-kubeconfig --region <region> --name <cluster_name>
   ```
7. Deployed app:
   ```
   kubectl apply -f deployment.yml
   kubectl apply -f service.yml
   ```
8. Waited for `EXTERNAL-IP` to appear in:
   ```
   kubectl get svc fastapi-service
   ```
9. Opened the public IP in browser to verify app.

---

## ✅ Status
Successfully deployed a Dockerized FastAPI app to AWS EKS via Kubernetes with LoadBalancer service.
