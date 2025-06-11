
# 🚀 FastAPI on AWS EKS (Kubernetes) with LoadBalancer Service

This project demonstrates deploying a **FastAPI** application to a production-grade **Kubernetes cluster** using **Amazon EKS** (Elastic Kubernetes Service) with an **external LoadBalancer**. The infrastructure is fully hosted on **AWS**, with Kubernetes-managed services and auto-scalable EC2 nodes.

---

## 📁 Project Structure

```bash
.
├── deployment.yml        # Kubernetes Deployment for FastAPI app
├── service.yml           # Kubernetes Service of type LoadBalancer
├── Dockerfile            # Dockerfile for FastAPI app (assumed)
└── README.md             # Project documentation
```

---

## ⚙️ Technologies Used

- 🌐 **FastAPI** (Python backend)
- 🐳 **Docker**
- ☸️ **Kubernetes (EKS)**
- 🛠️ **kubectl + AWS CLI**
- ☁️ **AWS**: EKS, EC2, VPC, IAM, Subnets, Load Balancer

---

## 🧑‍💻 What We've Done So Far

### ✅ FastAPI App
- A simple FastAPI backend (code not included here).

### ✅ Dockerization
- Dockerfile created for containerizing the app.
- Image pushed to **Docker Hub** (e.g., `mukul0412/fastapi-k8s-app:latest`).

### ✅ Kubernetes Manifests
- **`deployment.yml`**: Defines a `Deployment` with FastAPI running in pods.
- **`service.yml`**: Exposes the app using `Service` of type `LoadBalancer`.

### ✅ EKS Cluster Setup
- Created EKS cluster (`fastapi-cluster`) in region `ap-south-1`.
- Used:
  - `AmazonEKSClusterPolicy` for control plane
  - EC2 node group with appropriate IAM role
- VPC and subnets were automatically created (or configured manually).

### ✅ kubeconfig Setup
```bash
aws eks update-kubeconfig --region ap-south-1 --name fastapi-cluster
```

### ✅ Deployment on Cluster
```bash
kubectl apply -f deployment.yml
kubectl apply -f service.yml
```

---

## 📡 Service Status

```bash
kubectl get svc fastapi-service
```

Initially, the `EXTERNAL-IP` may be in `<pending>` status. This happens while AWS provisions a public Load Balancer. It usually takes a few minutes.

---

## ✅ To Do Next

- Add Ingress (optional)
- Add domain with Route 53 (optional)
- Add SSL with ACM and ALB Ingress Controller (production-grade)
- Monitor using Prometheus/Grafana

---
