# AI Operations Assignment

This repository contains the implementation for Questions 1–4 of the AI Operations assignment 2.

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
│── AiOps_Assignment_2_Report.pdf
├── README.md
└── AI_DISCLOSURE.md

```
# Q1 — Dockerized Spam Detection API

## Overview

The objective of Q1 was to build a REST API for spam detection and containerize it using Docker.

The spam classifier uses a **TF-IDF vectorizer** followed by a **Multinomial Naive Bayes** classifier. The trained model is saved as `model.joblib` and loaded by the FastAPI application.

The API provides two endpoints:

- `POST /predict` — predicts whether a message is `spam` or `ham`.
- `GET /healthz` — checks whether the API is running correctly.

---
### Q1

## Files Used and Description 

- spam_classifier.ipynb	Trains and evaluates the spam classification model
- model.joblib	Saved trained TF-IDF + Multinomial Naive Bayes pipeline
- app.py	FastAPI application providing /predict and /healthz
- Dockerfile.naive	Basic Docker image definition
- Dockerfile.multistage	Multi-stage Docker image definition
- requirements.txt	Python dependencies
- app_q1_backup.py	Backup copy of the API implementation
- docker_kubernetes.ipynb Builds the docker image 

## How to Run
* Navigate to the Q1-2 directory:
```bash
cd Q1-2
```
* Install the dependencies:
```bash
pip install -r requirements.txt
```
* Run the FastAPI application:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```
* The API can then be accessed at:
```bash
http://localhost:8000
```
* FastAPI's interactive documentation is available at:
```bash
http://localhost:8000/docs
```
* Train the Model
```Open and run spam_classifier.ipynb```
- This trains the spam classifier and saves the trained model as: model.joblib
* Build the Docker Images by opening and running docker_kubernetes.ipynb
- This builds both naive and multi stage docker images.


### Q2

## Files Used and Description 
- Same files as Q1 .

## How to run
Q2 is implemented in the same `docker_kubernetes.ipynb` notebook used for Q1.
* Open and run
```
docker_kubernetes.ipynb
```
* Run the notebook from the Q1 section first, followed by the Q2 section.
* The Q2 section starts the FastAPI application with Redis caching using Docker Compose.
* The Docker Compose stack can be started using:
```docker compose up --build```
* Send the same prediction request twice to observe the caching behaviour. The first request results in a cache miss, while the repeated request results in a cache hit.
* The notebook also measures the response times and calculates the caching speedup.

### Q3 - How to Run
* Navigate to the Q3 directory:
```bash
cd Q3
```
* Open and run:
```kubernetes_indexed.ipynb```
* Run the notebook cells one by one and in the given order, as each step depends on the previous one. The notebook:
   * Creates the 8 CSV shards.
   * Builds the Kubernetes worker Docker image.
   * Loads the image into Minikube.
   * Applies the Indexed Job.
   * Monitors the Job Pods and their execution.
   * Collects the results through the Kubernetes API.
* The Kubernetes cluster used for Q3 should be running before executing the Job.
* The final results can be collected using:
```python3 collect_results.py```
## Note : The execution of collect_results.py is also included as a cell inside kubernetes_indexed_job.ipynb. It does not need to be run separately if all notebook cells are executed in order.


### Q4 - How to Run
## Q4 — How to Run

* Navigate to the Q4 directory:
```bash
cd Q4
```
* Open and run:
```kubernetes_deployment.ipynb```
* Run the notebook cells one by one and in the given order, as each step depends on the previous one.
* The notebook:
    * Builds the initial v1 Docker image.
    * Loads the image into Minikube.
    * Creates the Kubernetes Deployment and Service.
    * Verifies the 2 running replicas and readiness probe.
    * Demonstrates self-healing by deleting a Pod and observing its replacement.
    * Builds and loads the v2 Docker image.
    * Performs the rolling update from v1 to v2.
    * Verifies the rollout status and history.
    * Checks the updated /healthz response.
* The Kubernetes cluster used for Q4 should be running before executing the notebook.
## Note: All the commands and steps required for Q4 are included as cells inside kubernetes_deployment.ipynb. No separate manual execution is required if the notebook is run from start to finish.

## Expected Results

### Q1 — Dockerized Spam Detection API
- Test accuracy: **1.00**
- Naive Docker image: **~2.28 GB**
- Multi-stage Docker image: **~718 MB**
- `/healthz` returns HTTP 200 with `{"status":"ok"}`
- `/predict` successfully returns `spam` or `ham`

### Q2 — Redis Caching & Docker Compose
- First request: **~0.071 seconds (cache miss)**
- Repeated request: **~0.002 seconds (cache hit)**
- Measured speedup: **~33.42×**
- Docker Compose successfully runs the FastAPI API and Redis cache.

### Q3 — Kubernetes Indexed Job
- **8/8** shards processed successfully
- **800** total rows processed
- **24** invalid rows
- **776** valid rows
- `parallelism: 4` enabled concurrent shard processing.

### Q4 — Kubernetes Deployment
- **2/2** API replicas running successfully
- Deleted Pods were automatically replaced by Kubernetes.
- Rolling update from **v1 → v2** completed successfully.
- Rollout history contains **2 revisions**.
- `/healthz` confirms the running application as **v2**.

## Technologies Used

- **Python** — Model training and API development
- **scikit-learn** — TF-IDF and Multinomial Naive Bayes
- **FastAPI** — REST API
- **Joblib** — Model serialization
- **Docker** — Containerization
- **Docker Compose** — Multi-container setup with Redis
- **Redis** — Prediction caching
- **Kubernetes** — Container orchestration
- **Minikube** — Local Kubernetes cluster
- **Jupyter Notebook** — Implementation and experimentation

## AI Disclosure

See [AI_DISCLOSURE.md](AI_DISCLOSURE.md) for details on how AI tools were used during the development of this assignment.


