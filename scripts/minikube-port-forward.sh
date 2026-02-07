#!/usr/bin/env bash
# Port-forward frontend (3000) and backend (8000) so you can open http://localhost:3000
# and login works (no ingress Host header issue). Run from project root.
# Stop with Ctrl+C.
set -e
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"
if ! minikube status &>/dev/null; then
  echo "Minikube not running. Run: ./scripts/minikube-setup.sh"
  exit 1
fi
echo "Forwarding backend 8000, frontend 3000..."
kubectl port-forward svc/todo-app-backend 8000:8000 &
PID1=$!
kubectl port-forward svc/todo-app-frontend 3000:3000 &
PID2=$!
trap "kill $PID1 $PID2 2>/dev/null; exit" INT TERM
sleep 2
echo "Open http://localhost:3000 (backend: http://localhost:8000). Press Ctrl+C to stop."
wait
