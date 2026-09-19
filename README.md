# AI Operations Assignment

This repository contains the implementation for Questions 1–4 of the AI Operations assignment.

The work covers:
- Dockerizing a spam detection REST API
- Redis caching and Docker Compose
- Kubernetes Indexed Jobs for batch processing
- Kubernetes Deployments for a long-running API
- Self-healing and rolling updates

---

# 1. Repository Structure

```text
Assignment/
│
├── Q1-2/
│   ├── app.py
│   ├── app_q1_backup.py
│   ├── docker-compose.yml
│   ├── Dockerfile.multistage
│   ├── Dockerfile.naive
│   ├── docker_kubernetes.ipynb
│   ├── model.joblib
│   ├── requirements.txt
│   └── spam_classifier.ipynb
│
├── Q3/
│   ├── shards/
│   │   ├── shard-0.csv
│   │   ├── shard-1.csv
│   │   ├── ...
│   │   └── shard-7.csv
│   ├── collect_results.py
│   ├── Dockerfile.job
│   ├── generate_shards.py
│   ├── job.yaml
│   ├── kubernetes_indexed_job.ipynb
│   └── validate_shard.py
│
├── Q4/
│   ├── app_k8s.py
│   ├── app_v2.py
│   ├── deployment.yaml
│   ├── Dockerfile.k8s
│   ├── Dockerfile.k8s.v2
│   ├── kubernetes_deployment.ipynb
│   ├── model.joblib
│   ├── requirements.txt
│   └── service.yaml
│
├── README.md
└── AI_DISCLOSURE.md
