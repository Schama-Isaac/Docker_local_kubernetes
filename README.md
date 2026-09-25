# MSc DE1 Distributed Systems - Docker & Local Kubernetes Project

## Objective
This project takes the public starter application from UBC, verifies it works locally, then builds a secure Docker image, publishes it to Docker Hub, and deploys it on a local Kind Kubernetes cluster.

## Original starter application
- Repository: https://github.com/ubc/flask-sample-app

## Prerequisites
- Docker
- Docker Hub account
- kubectl
- kind
- Python 3.12+

## 1) Run the original app locally
```bash
cd appsrc
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```
Then test:
- GET /
- GET /items
- GET /items/0
- POST /items

## 2) Run tests locally
```bash
cd appsrc
source .venv/bin/activate
python -m unittest discover -s tests -v
```

## 3) Build the Docker image
```bash
cd /path/to/project
docker build -t msc-de1-flask-app:local .
```

## 4) Run with Docker
```bash
docker run --rm -d -p 5001:5000 --name msc-de1-flask-app msc-de1-flask-app:local
curl http://localhost:5001/health
curl http://localhost:5001/items
```
Stop and remove:
```bash
docker stop msc-de1-flask-app
docker rm msc-de1-flask-app
```

## 5) Run with Docker Compose
```bash
docker compose up --build -d
docker compose ps
docker compose logs -f flask-app
curl http://localhost:5001/health
````
To stop:
```bash
docker compose down
```

## 6) Docker Hub publication
Build and tag the image:
```bash
docker build -t <dockerhub-user>/msc-de1-flask-app:1.0.0 -t <dockerhub-user>/msc-de1-flask-app:latest .
docker login
docker push <dockerhub-user>/msc-de1-flask-app:1.0.0
docker push <dockerhub-user>/msc-de1-flask-app:latest
```
Public repository URL: <to be filled>

## 7) Create the Kind cluster
```bash
kind create cluster --config kind/kind-config.yaml --name msc-de1-kind
kubectl cluster-info
```

If the image is still local, load it into the cluster:
```bash
kind load docker-image msc-de1-flask-app:local --name msc-de1-kind
```

## 8) Deploy to Kubernetes
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/network-policy.yaml
kubectl get pods -n msc-de1-project
kubectl get svc -n msc-de1-project
```
Access the app locally:
```bash
kubectl port-forward -n msc-de1-project svc/flask-app-service 8080:80
curl http://localhost:8080/health
```

## 9) Clean up
```bash
kubectl delete -f k8s/
kind delete cluster --name msc-de1-kind
```

## Verification commands and evidence

### Baseline validation before containerization
```bash
cd /Users/schamazannou/Documents/AIVANCITY/MScDE1/distributed_system/Docker_local_kubernetes_project
python3 -m unittest discover -s tests -v
```

### Docker image validation
```bash
docker image ls --format 'table {{.Repository}}\t{{.Tag}}\t{{.ID}}' | grep -E 'msc-de1-flask-app|zifs/msc-de1-flask-app'
```

### Kubernetes validation
```bash
kubectl get pods -n msc-de1-project -o wide
kubectl get svc -n msc-de1-project
```

### HTTP checks
```bash
kubectl port-forward -n msc-de1-project svc/flask-app-service 8080:80
curl -sS http://localhost:8080/health
curl -sS http://localhost:8080/items
```

### Security scan
```bash
docker scout cves zifs/msc-de1-flask-app:1.0.0
```

### Kubernetes behavior checks
```bash
kubectl scale deployment/flask-app-deployment -n msc-de1-project --replicas=3
kubectl rollout status deployment/flask-app-deployment -n msc-de1-project --timeout=180s
kubectl delete pod -n msc-de1-project "$OLD" --wait=false
kubectl get pods -n msc-de1-project -o wide
```

All the actual command outputs used as proof are saved in the evidence folder:

- [evidence/README.md](evidence/README.md)
- [evidence/screenshots-or-command-output](evidence/screenshots-or-command-output)

## Security decisions and limitations
- Application runs as a non-root user in Docker and Kubernetes.
- Linux capabilities are dropped in the pod.
- A security scan and SBOM are stored in the security folder.
- Local Kind networking may not enforce all NetworkPolicy features by default; this project documents the intended policy and the cluster can be extended with a CNI when needed.
