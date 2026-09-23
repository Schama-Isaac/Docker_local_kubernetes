# Distributed Systems Project Report

## 1. Project objective

This project aimed to take a basic Flask application, validate its behavior locally, containerize it with Docker, scan and harden it, publish the image to Docker Hub, and deploy it on a local Kubernetes cluster using Kind. The objective was not only to run the application, but also to demonstrate a complete DevOps workflow with security and deployment validation.

## 2. Application baseline and local validation

The starting application was a simple Flask service exposing a small in-memory item store. It was first validated locally before any containerization step.

### Validation performed

The application test suite was executed successfully with:

```bash
python3 -m unittest discover -s tests -v
```

Evidence from execution:

- 6 tests executed
- 6 tests passed
- result: OK

The tested behaviors included:

- root endpoint
- health endpoint
- item listing
- item retrieval
- non-existent item handling
- item creation

This confirmed that the application logic was valid before moving to Docker and Kubernetes layers.

## 3. Containerization with Docker

A production-oriented Docker image was created using a Dockerfile that:

- installs Python dependencies
- runs the application with Gunicorn
- exposes port 5000
- configures a non-root runtime user
- uses health checks
- avoids unnecessary privileges

The project also included a Compose definition used for local container validation.

### Docker build and image validation

The image was built locally and tagged as:

- `msc-de1-flask-app:local`
- `zifs/msc-de1-flask-app:1.0.0`
- `zifs/msc-de1-flask-app:latest`

This was verified by listing the local Docker images.

## 4. Security analysis and SBOM

The security section of the project included two key artifacts:

- `security/vulnerability-scan.txt`
- `security/sbom.spdx.json`

### SBOM generation

The SBOM was generated in SPDX format to provide a software bill of materials for the image. This gives traceability for packages included in the runtime environment and supports compliance-oriented review.

### Vulnerability scan

A Docker Scout scan was performed against the published image. The scan identified:

- 21 vulnerable packages
- 49 vulnerabilities total
- 7 HIGH
- 3 MEDIUM
- 40 LOW

This is a realistic outcome for a container image built on a base runtime image with transitive package dependencies. The analysis was therefore documented as a security review, not as a claim of zero-risk deployment.

The project explicitly reflects the security posture of the solution:

- app dependencies were updated to reduce risk
- the container runs as a non-root user
- a full scan and SBOM were created and retained in the repository
- the remaining vulnerabilities are documented rather than hidden

## 5. Docker Hub publication

The Docker image was pushed to Docker Hub under the repository:

- `zifs/msc-de1-flask-app`

This step completed the pipeline from local development to external image hosting and made the artifact available for cluster deployment.

## 6. Kubernetes deployment using Kind

A local Kubernetes cluster was created with Kind, configured through the file `kind/kind-config.yaml`.

### Cluster configuration

The cluster used:

- 1 control-plane node
- 2 worker nodes

### Kubernetes manifests

The project includes a proper K8s deployment structure:

- `k8s/namespace.yaml`
- `k8s/deployment.yaml`
- `k8s/service.yaml`
- `k8s/network-policy.yaml`

The deployment defined:

- 2 replicas
- rolling update strategy
- readiness and liveness probes
- resource requests and limits
- non-root security context
- read-only root filesystem
- dropped Linux capabilities

The service exposed the application internally via a ClusterIP service. The network policy restricted ingress and egress as expected for a simple Kubernetes environment.

### Deployment validation

The cluster was created and the manifests were applied successfully.

Validation commands performed:

```bash
kubectl wait --for=condition=Available deployment/flask-app-deployment -n msc-de1-project --timeout=180s
kubectl get pods -n msc-de1-project -o wide
```

Evidence from execution:

- Deployment condition met
- 2 pods running
- READY = 1/1 for both replicas

The application was then exposed locally with port-forwarding and validated over HTTP:

```bash
kubectl port-forward -n msc-de1-project svc/flask-app-service 8080:80
curl http://localhost:8080/health
curl http://localhost:8080/items
```

Observed output:

```json
{"status":"ok"}
{"items":[]}
```

This confirms the application was not only deployed, but actually responding correctly inside the Kubernetes cluster.

## 7. Repository structure and deliverables

The final project includes the key artifacts expected for a complete distributed systems delivery:

- application source code
- tests
- Dockerfile
- Docker Compose definition
- security scan report
- SBOM
- Kubernetes manifests
- Kind cluster configuration
- project README and final report

## 8. Key lessons and conclusions

This project demonstrates a complete application lifecycle from local development to secure container deployment and local orchestration:

1. The application logic was validated before infrastructure work.
2. The Docker image was built and published to Docker Hub.
3. Security was evaluated using scan results and an SPDX SBOM.
4. A local Kubernetes cluster was provisioned with Kind.
5. The deployment was validated end-to-end with health checks and HTTP requests.

The overall result is a functional and well-documented distributed systems deployment, with transparent security risks clearly reported instead of ignored.

## 9. Final assessment

The project successfully met the requested objectives of:

- local validation of the app
- Dockerization
- security review and SBOM generation
- publication to Docker Hub
- local Kubernetes deployment with Kind
- verification of runtime behavior

The technical workflow is complete, and the project is ready for final submission and reporting.
