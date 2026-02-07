# Tasks: Minikube Deployment

**Input**: Design documents from `specs/phase-4-local-kubernetes/003-minikube-deployment/`
**Prerequisites**: spec.md ✅, plan.md ✅
**Branch**: `phase4-003-minikube-deployment`

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Exact file paths included in descriptions

## Path Conventions

- **Scripts**: `scripts/`
- **Chart**: `helm/todo-app/`
- **Root**: project root for README.md

---

## Phase 1: Minikube Setup (US1)

**Goal**: Script and docs to start Minikube with ingress addon.

**Independent Test**: Run script; `kubectl get nodes` shows Ready; `minikube addons list` shows ingress enabled.

### Implementation for User Story 1

- [x] T001 [US1] Create `scripts/minikube-setup.sh`: minikube start (--cpus=4 --memory=8192 --driver=docker)
- [x] T002 [US1] In `minikube-setup.sh`: enable ingress addon; optional metrics-server
- [x] T003 [US1] In script: verify cluster (kubectl get nodes); make script executable (chmod +x)
- [x] T004 [US1] Add README subsection "Minikube setup" with prerequisites and how to run script

**Checkpoint**: Minikube starts; ingress addon enabled; README documents setup

---

## Phase 2: Build and Load Images (US1)

**Goal**: Backend and frontend images built and available to Minikube.

**Independent Test**: After running build/load steps, images exist in Minikube (e.g. minikube image list or eval minikube docker-env + docker images).

### Implementation for User Story 1

- [x] T005 [US1] Document or add to script: build backend image `docker build -t todo-backend:latest ./backend`
- [x] T006 [US1] Document or add to script: build frontend image `docker build -t todo-frontend:latest ./frontend`
- [x] T007 [US1] Document or script: load images into Minikube (eval $(minikube docker-env) then build, OR minikube image load after build)
- [x] T008 [US1] Ensure values-minikube or chart uses image tag/pullPolicy so Minikube uses local images

**Checkpoint**: Images todo-backend:latest and todo-frontend:latest available to Minikube

---

## Phase 3: Deploy with Helm (US1)

**Goal**: Helm install/upgrade with chart + values-minikube + secrets; pods Running.

**Independent Test**: `helm list` shows todo-app; `kubectl get pods` shows backend and frontend Running.

### Implementation for User Story 1

- [x] T009 [US3] Create `scripts/deploy-minikube.sh`: call minikube-setup (or assume up), build images, load into Minikube
- [x] T010 [US3] In deploy script: helm upgrade --install todo-app helm/todo-app -f helm/todo-app/values-minikube.yaml with --set secret.databaseUrl, secret.betterAuthSecret, secret.openaiApiKey (from env or .env file)
- [x] T011 [US3] Script: fail fast if required env vars missing; document required vars in README
- [x] T012 [US3] Add README subsection "Deploy to Minikube" with example helm install and secret passing
- [x] T013 [US3] Test: Run deploy (with real secrets); kubectl get pods shows both pods Running

**Checkpoint**: Release installed; all pods Running; README has deploy instructions

---

## Phase 4: Ingress Access (US1)

**Goal**: User can open app in browser via Ingress host.

**Independent Test**: Browser can open frontend URL; backend /health returns 200 via same host or port-forward.

### Implementation for User Story 1

- [x] T014 [US1] Add README subsection "Access the app": Ingress host (e.g. todo.minikube.local), minikube ip, add to /etc/hosts
- [x] T015 [US1] Optional: in deploy script, echo "Add to /etc/hosts: $(minikube ip) todo.minikube.local"
- [x] T016 [US1] Test: Add /etc/hosts entry; open http://todo.minikube.local (or http://$(minikube ip)); frontend loads

**Checkpoint**: App accessible in browser; backend API reachable (e.g. /api/health)

---

## Phase 5: Verification and Documentation (US2, US3)

**Goal**: Verify app behavior unchanged; optional AIOps; README complete.

**Independent Test**: Sign in, create/list/update/delete/complete tasks, use AI chat; all work. Optional: one kubectl-ai/Kagent use documented.

### Implementation for User Story 2 & 3

- [x] T017 [US2] Add README "Verify Minikube deployment": pods Running, health endpoints, sign in, tasks, AI chat
- [x] T018 [US2] Test: Sign in, create task, list tasks, use chat "Add a task to test"; confirm MCP tools work
- [x] T019 [US2] Test: Backend /health and /ready return 200 (curl via Ingress or port-forward)
- [x] T020 [P] [US3] Optional: Use kubectl-ai or Kagent once; document command and result in PHR or README
- [x] T021 Update README Table of Contents if new section added; ensure "Minikube Deployment" is findable

**Checkpoint**: All verification steps pass; README Minikube section complete; optional AIOps documented

---

## Task Details

### T001–T003: minikube-setup.sh

**File**: `scripts/minikube-setup.sh`

Example structure:

```bash
#!/usr/bin/env bash
set -e
minikube start --cpus=4 --memory=8192 --driver=docker
minikube addons enable ingress
# minikube addons enable metrics-server  # optional
kubectl get nodes
echo "Minikube ready. Run: kubectl cluster-info"
```

- Make executable: `chmod +x scripts/minikube-setup.sh`

---

### T005–T007: Build and Load

- Build from **project root**: `docker build -t todo-backend:latest ./backend`, `docker build -t todo-frontend:latest ./frontend`.
- Load: either
  - `eval $(minikube docker-env)` then run the same docker build commands (build inside Minikube’s Docker), or
  - `minikube image load todo-backend:latest` and `minikube image load todo-frontend:latest` after building on host.

---

### T009–T011: deploy-minikube.sh

**File**: `scripts/deploy-minikube.sh`

- Source or run minikube-setup if desired; ensure Minikube is up.
- Build images (with or without minikube docker-env) and ensure they are available to Minikube.
- Require env: DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY (or read from .env).
- Run: `helm upgrade --install todo-app helm/todo-app -f helm/todo-app/values-minikube.yaml --set secret.databaseUrl="$DATABASE_URL" --set secret.betterAuthSecret="$BETTER_AUTH_SECRET" --set secret.openaiApiKey="$OPENAI_API_KEY"`.
- Optionally: `kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=todo-app --timeout=120s`.

---

### T014–T015: Access the app

- Ingress host in values-minikube: `todo.minikube.local`.
- Get IP: `minikube ip`.
- Add to /etc/hosts: `<minikube-ip> todo.minikube.local`.
- URL: http://todo.minikube.local (or http://<minikube-ip> if not using host).

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Minikube setup)
        ↓
Phase 2 (Build & load images)
        ↓
Phase 3 (Helm deploy)
        ↓
Phase 4 (Ingress access)
        ↓
Phase 5 (Verification & docs)
```

### Task Dependencies

- T001–T004: Minikube setup and README setup subsection.
- T005–T008: Require Minikube up; images for Phase 3.
- T009–T013: Require images; produce running pods.
- T014–T016: Require release installed; document and test access.
- T017–T021: Can run after app is accessible.

---

## Verification Commands

### After setup
```bash
kubectl get nodes
minikube addons list | grep ingress
```

### After deploy
```bash
helm list
kubectl get pods
kubectl get ingress
```

### Health
```bash
# Port-forward if needed:
kubectl port-forward svc/todo-app-backend 8000:8000 &
curl http://localhost:8000/health
curl http://localhost:8000/ready
```

### Access
```bash
minikube ip
# Add to /etc/hosts: <ip> todo.minikube.local
# Open http://todo.minikube.local
```

---

## Completion Checklist

Before marking feature complete:

- [x] Minikube setup script exists and runs
- [x] Deploy script builds/loads images and runs helm install with secrets
- [ ] All pods Running (run deploy script with real secrets to verify)
- [ ] Ingress configured; app accessible in browser (add /etc/hosts and open URL)
- [ ] Backend /health and /ready return 200
- [ ] Frontend /api/health returns 200
- [ ] User can sign in and use tasks
- [ ] AI chat and MCP tools work
- [x] README includes Minikube setup, deploy, access, and verification
- [x] No application code changes
- [x] Optional: AIOps (kubectl-ai/Kagent) used and documented

---

## Notes

- [P] tasks = can run in parallel where noted
- Secrets: never commit; use env or gitignored file
- Database (Neon) is external; cluster must have network access
- **CRITICAL**: No business logic or app code changes

---

## Post-Completion

After all tasks complete:
1. Run `/sp.skill-learner` to capture learnings
2. Create PHR for this feature
3. Phase 4 is complete; next: Phase V (cloud, Kafka, Dapr) per hackathon doc
