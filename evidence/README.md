# Evidence and verification commands

This folder contains the actual command output used to validate the project at each major stage.

## 1. Baseline validation

Command executed:

```bash
cd /Users/schamazannou/Documents/AIVANCITY/MScDE1/distributed_system/Docker_local_kubernetes_project
python3 -m unittest discover -s tests -v
```

Output recorded in:

- evidence/screenshots-or-command-output/01_baseline_tests.txt

## 2. Docker validation

Command executed:

```bash
docker image ls --format 'table {{.Repository}}\t{{.Tag}}\t{{.ID}}' | grep -E 'msc-de1-flask-app|zifs/msc-de1-flask-app'
```

Output recorded in:

- evidence/screenshots-or-command-output/02_docker_images.txt

## 3. Kubernetes validation

Commands executed:

```bash
kubectl get pods -n msc-de1-project -o wide
kubectl get svc -n msc-de1-project
```

Output recorded in:

- evidence/screenshots-or-command-output/03_k8s_pods.txt
- evidence/screenshots-or-command-output/04_k8s_services.txt

## 4. HTTP endpoint validation

Commands executed:

```bash
kubectl port-forward -n msc-de1-project svc/flask-app-service 8080:80
curl -sS http://localhost:8080/health
curl -sS http://localhost:8080/items
```

Output recorded in:

- evidence/screenshots-or-command-output/05_http_checks.txt

## 5. Security validation

Command executed:

```bash
docker scout cves zifs/msc-de1-flask-app:1.0.0
```

Summary recorded in:

- evidence/screenshots-or-command-output/06_security_scan_summary.txt

## 6. Kubernetes behavior validation

Commands executed:

```bash
kubectl scale deployment/flask-app-deployment -n msc-de1-project --replicas=3
kubectl rollout status deployment/flask-app-deployment -n msc-de1-project --timeout=180s
kubectl delete pod -n msc-de1-project "$OLD" --wait=false
kubectl get pods -n msc-de1-project -o wide
```

This demonstrates the expected Kubernetes properties:

- scaling
- self-healing
- controlled rollout behavior

## Notes

The evidence folder is intentionally kept as a proof archive for the project and is referenced by the report in the final submission.
