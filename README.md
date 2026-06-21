# TechKraft DevOps Assessment Submission

## Candidate Information

**Name:** Shramik Awale

**GitHub:** https://github.com/shramikawale

**LinkedIn:** https://www.linkedin.com/in/shramik-awale/

**Email:** [shramikawale@gmail.com](mailto:shramikawale@gmail.com)

---

# Repository Structure

```text
.
├── README.md
├── part1-terraform/
│   └── analysis.md
├── part2-linux/
│   ├── troubleshooting.md
│   └── Dockerfile
├── part3-python/
│   ├── ec2_monitor.py
│   └── config.json
├── part4-bash/
│   └── analyze_nginx_logs.sh
├── part5-network/
│   └── architecture.md
├── part6-cicd/
│   └── improvements.md
└── k8s/
    └── deployment.yaml
```

---

# Solution Overview

## Part 1 – Terraform Review (`part1-terraform/analysis.md`)

This section contains an analysis of the provided Terraform code, including:

* Security issues identified in the current Terraform configuration
* Architectural problems in the current design
* Recommended changes for production-readiness from a DevSecOps and infrastructure perspective

Key topics covered:

* Open security group risks
* Missing private/public subnet separation
* Lack of ALB/ASG design
* Missing IAM/security hardening
* Production-grade infrastructure improvements

---

## Part 2 – Linux / Docker (`part2-linux/`)

This section includes:

* **`troubleshooting.md`** → Linux troubleshooting and operational notes
* **`Dockerfile`** → Production-ready multi-stage Dockerfile for a Flask application

Docker solution includes:

* Python 3.11 base image
* Multi-stage build (builder + runtime)
* Support for compiling dependencies/C extensions
* Non-root container user
* Health check support
* Gunicorn-based startup command for production use

---

## Part 3 – Python Script Design (`part3-python/`)

This section includes:

* **`ec2_monitor.py`** → Python script using boto3 to monitor EC2 instances and CloudWatch CPU metrics
* **`config.json`** → External configuration file for thresholds, regions, and notification settings

Script features:

* Lists all running EC2 instances
* Retrieves CPU metrics for the last 1 hour at 5-minute intervals
* Calculates average, minimum, and maximum CPU utilization
* Flags instances above threshold
* Exports results to JSON
* Includes argparse, logging, type hints, and error handling

---

## Part 4 – Bash Log Analysis (`part4-bash/analyze_nginx_logs.sh`)

This section contains a Bash script to analyze Nginx access logs.

Features:

* Parses Nginx access logs from a provided file path
* Shows top 10 IPs by request count
* Calculates percentage of 4xx and 5xx errors
* Displays top 10 most accessed endpoints
* Outputs a formatted summary report
* Handles missing or malformed entries gracefully using standard Linux tools only

---

## Part 5 – Network Architecture Design (`part5-network/architecture.md`)

This section contains the DNS architecture design for TechKraft using AWS Route 53.

Topics covered:

* Redundant DNS architecture design
* Primary/secondary failover using Route 53
* Health check strategy
* Low-latency design considerations for Nepal / South Asia
* Cost optimization considerations
* Estimated implementation timeline

---

## Part 6 – CI/CD Improvements (`part6-cicd/improvements.md`)

This section reviews the provided GitHub Actions workflow and proposes a production-ready CI/CD design.

Topics covered:

* Existing pipeline issues
* Security scanning recommendations
* Testing strategy improvements
* Approval gates
* Rollback mechanisms
* Environment promotion flow (dev → staging → prod)

Recommended tools include:

* SonarQube
* Trivy
* Checkov
* Gitleaks
* ArgoCD / Argo Rollouts

---

## Bonus – Kubernetes (`k8s/deployment.yaml`)

This section contains a Kubernetes deployment manifest for the Flask application.

Included resources:

* ConfigMap
* Deployment
* Service
* HorizontalPodAutoscaler

Features:

* Minimum 2 replicas
* CPU/memory resource requests and limits
* Liveness and readiness probes
* Environment variables loaded from ConfigMap

---

# Assumptions Made

* AWS account and permissions are already configured for the Python monitoring script.
* The Flask application exposes a `/health` endpoint for health checks in Docker and Kubernetes.
* Nginx access logs follow a standard or near-standard access log format where IP, request, and status fields are available.
* The Route 53 DNS design assumes the primary region for Nepal users is **ap-south-1 (Mumbai)** and secondary failover region is **ap-southeast-1 (Singapore)**.
* CI/CD recommendations are designed for a production-grade environment and may be adapted based on company-specific tooling and deployment strategy.

---

# Time Spent Per Section

| Section | Task                                             | Approx. Time |
| ------- | ------------------------------------------------ | ------------ |
| Part 1  | Terraform Review & Production Readiness Analysis | 45 mins      |
| Part 2  | Dockerfile + Linux Troubleshooting Notes         | 30 mins      |
| Part 3  | Python Monitoring Script                         | 45 mins      |
| Part 4  | Bash Log Analysis Script                         | 25 mins      |
| Part 5  | Network Architecture Design                      | 35 mins      |
| Part 6  | CI/CD Pipeline Review & Improvements             | 30 mins      |
| Bonus   | Kubernetes Deployment Manifest                   | 20 mins      |

**Total Estimated Time:** ~3.5 to 4 hours

---

# Tools / Versions Used

* **Terraform** – v1.x concepts
* **AWS** – Route 53, EC2, CloudWatch, boto3, ALB, Auto Scaling
* **Python** – 3.11
* **boto3** – AWS SDK for Python
* **Docker** – Multi-stage build with Python 3.11 slim image
* **Kubernetes** – Deployment, Service, HPA, ConfigMap
* **Bash / Linux tools** – awk, sed, sort, uniq, wc
* **GitHub Actions** – CI/CD workflow design
* **Security / DevSecOps tools referenced** – SonarQube, Trivy, Checkov, Gitleaks, ArgoCD

---

## Leadership & Mentorship Approach

As TechKraft has a team of 11 engineers, my focus would be:

- Terraform module standardization  
- GitOps adoption  
- AWS Well-Architected reviews  
- Security-first engineering practices  
- Incident response playbooks  
- Observability-driven operations  
- Internal DevOps workshops  
- Documentation-first culture  

This approach improves delivery speed, system reliability, and operational maturity while significantly reducing infrastructure and security risks across environments.

---

# Notes

This repository contains my solutions for the TechKraft DevOps assessment. I focused on providing production-oriented answers with emphasis on **security, reliability, automation, and operational readiness**.
