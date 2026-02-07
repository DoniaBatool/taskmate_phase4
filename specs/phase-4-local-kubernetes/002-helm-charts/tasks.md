# Tasks: Helm Charts

**Input**: Design documents from `specs/phase-4-local-kubernetes/002-helm-charts/`
**Prerequisites**: spec.md ✅, plan.md ✅
**Branch**: `phase4-002-helm-charts`

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Exact file paths included in descriptions

## Path Conventions

- **Helm chart**: `helm/todo-app/`
- **Templates**: `helm/todo-app/templates/`

---

## Phase 1: Chart Skeleton and Values (US1)

**Goal**: Create Chart metadata, default values, Minikube values, and shared helpers.

**Independent Test**: `helm lint helm/todo-app` (after templates exist)

### Implementation for User Story 1

- [x] T001 [P] [US1] Create `helm/todo-app/Chart.yaml` with name, version, appVersion
- [x] T002 [US1] Create `helm/todo-app/values.yaml` with image, replicas, resources, ingress, env placeholders
- [x] T003 [US1] Create `helm/todo-app/values-minikube.yaml` with Minikube ingress host and frontend API URL
- [x] T004 [US1] Create `helm/todo-app/templates/_helpers.tpl` with common labels and helpers

**Checkpoint**: Chart skeleton exists; `helm lint` runs (warnings only until templates added)

---

## Phase 2: Backend and Frontend Resources (US1, US2)

**Goal**: Add Deployments and Services with health probes.

**Independent Test**: `helm template helm/todo-app` produces valid Deployment and Service manifests

### Implementation for User Story 1 & 2

- [x] T005 [US1] Create `helm/todo-app/templates/backend-deployment.yaml` with liveness /health, readiness /ready
- [x] T006 [US1] Create `helm/todo-app/templates/backend-service.yaml` (ClusterIP, port 8000)
- [x] T007 [US1] Create `helm/todo-app/templates/frontend-deployment.yaml` with liveness /api/health
- [x] T008 [US1] Create `helm/todo-app/templates/frontend-service.yaml` (ClusterIP, port 3000)
- [x] T009 [US1] Test: Run `helm lint helm/todo-app` and fix any errors
- [x] T010 [US1] Test: Run `helm template helm/todo-app` and verify all resources render

**Checkpoint**: Deployments and Services render; helm lint passes

---

## Phase 3: ConfigMap, Secret, and Ingress (US3)

**Goal**: Add configuration and ingress for Minikube access.

### Implementation for User Story 3

- [x] T011 [US3] Create `helm/todo-app/templates/configmap.yaml` for non-secret env (if needed)
- [x] T012 [US3] Create `helm/todo-app/templates/secret.yaml` (values-driven; no real secrets in repo)
- [x] T013 [US3] Create `helm/todo-app/templates/ingress.yaml` (path / -> frontend, /api -> backend)
- [x] T014 [US3] Test: Run `helm template helm/todo-app -f helm/todo-app/values-minikube.yaml` and verify Ingress host

**Checkpoint**: ConfigMap, Secret, Ingress render; values-minikube applies correctly

---

## Phase 4: Validation & Documentation

**Goal**: Chart ready for 003-minikube-deployment; docs updated.

### Validation Tasks

- [x] T015 [P] Verify `helm lint helm/todo-app` passes with no errors
- [x] T016 [P] Verify `helm template` with default and values-minikube produces valid YAML
- [x] T017 Update README.md with Helm section (lint, template, link to Minikube deploy)

**Checkpoint**: Chart complete; ready for Minikube deployment (Feature 003)

---

## Task Details

### T001: Chart.yaml

**File**: `helm/todo-app/Chart.yaml`

```yaml
apiVersion: v2
name: todo-app
description: Todo Chatbot - Frontend and Backend
type: application
version: 0.1.0
appVersion: "1.0.0"
```

---

### T002: values.yaml

**File**: `helm/todo-app/values.yaml`

Key sections:
- `backend.image` (repository, tag, pullPolicy)
- `frontend.image` (repository, tag, pullPolicy)
- `backend.replicas`, `frontend.replicas`
- `backend.resources`, `frontend.resources`
- `backend.env` / `frontend.env` (placeholders or refs to Secret)
- `ingress.enabled`, `ingress.host`
- `secret.existingSecret` or `secret.create` and key names (no literal secret data)

---

### T003: values-minikube.yaml

**File**: `helm/todo-app/values-minikube.yaml`

- Override `ingress.host` for Minikube (e.g. todo.minikube.local)
- Set `frontend.env.NEXT_PUBLIC_API_URL` so browser can reach backend (e.g. http://backend.todo-app.svc:8000 or Ingress URL)

---

### T004: _helpers.tpl

**File**: `helm/todo-app/templates/_helpers.tpl`

- Define `todo-app.labels` (app.kubernetes.io/name, app.kubernetes.io/instance, etc.)
- Optional: `todo-app.backend.labels`, `todo-app.frontend.labels` for selectors

---

### T005: backend-deployment.yaml

- Use image from `values.backend.image`
- Env from ConfigMap/Secret as per values
- Liveness: httpGet path /health, port 8000
- Readiness: httpGet path /ready, port 8000
- initialDelaySeconds/periodSeconds appropriate for startup

---

### T006: backend-service.yaml

- ClusterIP Service
- selector matching backend Deployment labels
- port 8000, targetPort 8000

---

### T007: frontend-deployment.yaml

- Use image from `values.frontend.image`
- Env (e.g. NEXT_PUBLIC_API_URL from values)
- Liveness: httpGet path /api/health, port 3000

---

### T008: frontend-service.yaml

- ClusterIP Service
- selector matching frontend Deployment labels
- port 3000, targetPort 3000

---

### T012: secret.yaml

- Do not store real secrets in repo
- Use `existingSecret` from values, OR create Secret with keys (e.g. database-url, better-auth-secret, openai-api-key) and document that user supplies values at install time via --set or secret file

---

### T013: ingress.yaml

- Conditional: `{{- if .Values.ingress.enabled }}`
- Host from `.Values.ingress.host`
- Path / -> frontend service:3000
- Path /api -> backend service:8000 (path rewrite or prefix as needed for FastAPI)

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Chart skeleton)
        ↓
Phase 2 (Deployments & Services)
        ↓
Phase 3 (ConfigMap, Secret, Ingress)
        ↓
Phase 4 (Validation & docs)
```

### Task Dependencies

- T001–T004: Can be done in any order (all [P] or sequential)
- T005–T008: Depend on _helpers.tpl and values; T005/T006 can run in parallel with T007/T008
- T011–T013: Depend on Phase 2 for service names
- T015–T017: After all templates exist

---

## Verification Commands

### Lint

```bash
helm lint helm/todo-app
```

### Template (default values)

```bash
helm template todo-app helm/todo-app
```

### Template (Minikube)

```bash
helm template todo-app helm/todo-app -f helm/todo-app/values-minikube.yaml
```

### Dry-run install (no cluster needed)

```bash
helm install todo-app helm/todo-app --dry-run --debug
```

---

## Completion Checklist

Before marking feature complete:

- [x] All 17 tasks completed
- [x] helm lint helm/todo-app passes
- [x] helm template produces valid manifests for backend/frontend Deployment, Service, Ingress, ConfigMap, Secret
- [x] values-minikube.yaml present and used for Minikube
- [x] No application code or Dockerfiles modified
- [x] README updated with Helm instructions (or link to 003)

---

## Notes

- [P] tasks = different files, can run in parallel where noted
- Commit after each task or logical group
- Chart is consumed by 003-minikube-deployment for actual deploy
- **CRITICAL**: No business logic or app code changes

---

## Post-Completion

After all tasks complete:
1. Run `/sp.skill-learner` to capture learnings
2. Create PHR for this feature
3. Move to next feature: `003-minikube-deployment`
