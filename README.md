
# FastAPI Kubernetes Deployment on Amazon EKS

This project demonstrates how to containerize a FastAPI application, push the image to Docker Hub, and deploy it on a Kubernetes cluster using Amazon EKS (Elastic Kubernetes Service).

---

## 🧠 Project Stack

- **FastAPI** (Python web framework)
- **Docker** (for containerization)
- **Docker Hub** (image registry)
- **Kubernetes** (orchestration)
- **Amazon EKS** (managed Kubernetes service)
- **AWS IAM, VPC, EC2, Security Groups** (for cluster setup)

---

## 🚀 Project Structure

```
.
├── main.py
├── requirements.txt
├── Dockerfile
├── deployment.yml
├── service.yml
```

---

## 🛠️ Step-by-Step Guide

### 1. Create the FastAPI App (`main.py`)

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

---

### 2. Create `requirements.txt`

```
fastapi
uvicorn[standard]
```

---

### 3. Create the Dockerfile

```Dockerfile
# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### 4. Build and Push Docker Image

```bash
docker build -t mukul0412/fastapi-k8s-app:latest .
docker push mukul0412/fastapi-k8s-app:latest
```

---

### 5. Create Kubernetes Manifests

#### `deployment.yml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
      - name: fastapi
        image: mukul0412/fastapi-k8s-app:latest
        ports:
        - containerPort: 8000
```

#### `service.yml`

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
    - protocol: TCP
      port: 80
      targetPort: 8000
```

---

### 6. Create and Configure EKS Cluster

- Created EKS cluster with **Auto Mode**
- Configured **Cluster IAM Role** with required policies:
  - `AmazonEKSBlockStoragePolicy`
  - `AmazonEKSComputePolicy`
  - `AmazonEKSLoadBalancingPolicy`
  - `AmazonEKSNetworkingPolicy`
- Node IAM Role with EC2 permissions and correct trust relationship (`sts:TagSession`).
- Selected public subnets from default VPC

---

### 7. Connect kubectl to EKS

```bash
aws eks update-kubeconfig --region ap-south-1 --name fastapi-cluster
kubectl get nodes
```

---

### 8. Deploy to Kubernetes

```bash
kubectl apply -f deployment.yml
kubectl apply -f service.yml
```

Check service:

```bash
kubectl get svc fastapi-service
```

> **Note**: LoadBalancer external IP may take a few minutes to provision.

---

## ✅ Status

✅ EKS Cluster running  
✅ FastAPI Pods deployed  
🔄 LoadBalancer external IP pending (due to security group or subnet settings)

---

## 🔐 To Fix LoadBalancer Pending

- Ensure EKS worker node security group allows inbound traffic on port 80 from 0.0.0.0/0
- Ensure public subnets have route to an internet gateway
- Use AWS Load Balancer Controller for more control (optional)

---

## 📦 Next Steps

- Fix external access issue  
- Add domain via Route 53  
- Use HTTPS with ACM  
- Add CI/CD with GitHub Actions

---

## 👤 Author

**Mukul Bhardwaj**  
- [LinkedIn](https://www.linkedin.com/in/mukulbhardwaj0412)  
- [GitHub](https://github.com/MukulB0412)

