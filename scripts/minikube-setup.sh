#!/usr/bin/env bash
# Minikube setup for Todo Chatbot Phase 4 (003-minikube-deployment)
# Starts Minikube with ingress addon; run from project root.
set -e

# 4GB is enough for this app (2 pods: backend + frontend). Increase if Docker has more.
echo "Starting Minikube (cpus=2, memory=4096, driver=docker)..."
minikube start --cpus=2 --memory=4096 --driver=docker

echo "Enabling ingress addon..."
minikube addons enable ingress

echo "Enabling metrics-server (optional)..."
minikube addons enable metrics-server 2>/dev/null || true

echo "Verifying cluster..."
kubectl get nodes
echo ""
echo "Minikube ready. Run: kubectl cluster-info"
