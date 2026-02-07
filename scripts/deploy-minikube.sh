#!/usr/bin/env bash
# Deploy Todo Chatbot to Minikube (Phase 4 - 003-minikube-deployment)
# Builds images inside Minikube Docker, installs Helm chart with secrets.
# Run from project root. Requires: DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY
set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# --- Load secrets from .env if not already set ---
# Try docker/.env first, then backend/.env
if [ -z "$DATABASE_URL" ] || [ -z "$BETTER_AUTH_SECRET" ] || [ -z "$OPENAI_API_KEY" ]; then
  if [ -f "docker/.env" ]; then
    echo "Loading DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY from docker/.env"
    set -a
    source docker/.env
    set +a
  elif [ -f "backend/.env" ]; then
    echo "Loading from backend/.env"
    set -a
    source backend/.env
    set +a
  fi
fi

if [ -z "$DATABASE_URL" ] || [ -z "$BETTER_AUTH_SECRET" ] || [ -z "$OPENAI_API_KEY" ]; then
  echo "Error: Required env vars must be set: DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY"
  echo "  Option 1: Put them in docker/.env then run: ./scripts/deploy-minikube.sh"
  echo "  Option 2: export DATABASE_URL=... BETTER_AUTH_SECRET=... OPENAI_API_KEY=... then run the script"
  exit 1
fi

# --- Ensure Minikube is running ---
if ! minikube status &>/dev/null; then
  echo "Minikube not running. Run: ./scripts/minikube-setup.sh"
  exit 1
fi

# --- Build on host Docker (has working DNS), then load into Minikube ---
# Building inside Minikube's daemon often fails with "no such host" for registry-1.docker.io
echo "Building backend image (on host Docker)..."
docker build -t todo-backend:latest ./backend

echo "Building frontend image (on host Docker)..."
# Force rebuild so api.ts same-origin fix is included (cached layers skip npm run build)
docker build --no-cache -t todo-frontend:latest ./frontend

echo "Loading images into Minikube..."
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

# --- Helm install with secrets ---
echo "Installing/upgrading Helm release todo-app..."
helm upgrade --install todo-app helm/todo-app \
  -f helm/todo-app/values-minikube.yaml \
  --set secret.databaseUrl="$DATABASE_URL" \
  --set secret.betterAuthSecret="$BETTER_AUTH_SECRET" \
  --set secret.openaiApiKey="$OPENAI_API_KEY"

echo "Waiting for pods to be ready (timeout 120s)..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=todo-app --timeout=120s 2>/dev/null || true

echo ""
echo "Deploy complete. Pods:"
kubectl get pods -l app.kubernetes.io/instance=todo-app
echo ""
MINIKUBE_IP=$(minikube ip 2>/dev/null || true)
if [ -n "$MINIKUBE_IP" ]; then
  echo "Add to /etc/hosts: $MINIKUBE_IP todo.minikube.local"
  echo "Then open: http://todo.minikube.local"
fi
