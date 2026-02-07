# Implementation Plan: Helm Charts

**Branch**: `phase4-002-helm-charts` | **Date**: 2026-02-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/phase-4-local-kubernetes/002-helm-charts/spec.md`

## Summary

Create a Helm chart for the Todo Chatbot that packages frontend and backend into Kubernetes Deployments, Services, Ingress, ConfigMap, and Secret. Chart must support Minikube and pass `helm lint`. **NO application code changes.**

## Technical Context

**Prerequisite**: Feature 001-containerization complete (Docker images: todo-backend, todo-frontend)
**Primary Dependencies**: Helm 3, Kubernetes 1.24+
**Target Platform**: Minikube (values-minikube.yaml)
**Project Type**: Monorepo; single Helm chart for full stack
**Constraints**: No application code or Dockerfile changes

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| IX. Helm-Based Package Management | ✅ Pass | Helm charts for all services, minikube support |
| I. Spec-Driven Development | ✅ Pass | Spec created before plan |
| VI. AI Chatbot Architecture | ✅ Protected | No changes to app |
| VII. Container-First Deployment | ✅ Pass | Charts use existing images from 001 |

## Project Structure

### New Directories and Files

```text
helm/
└── todo-app/
    ├── Chart.yaml
    ├── values.yaml
    ├── values-minikube.yaml
    └── templates/
        ├── _helpers.tpl
        ├── backend-deployment.yaml
        ├── backend-service.yaml
        ├── frontend-deployment.yaml
        ├── frontend-service.yaml
        ├── ingress.yaml
        ├── configmap.yaml
        └── secret.yaml
```

**No changes** to `backend/`, `frontend/`, or `docker/`.

## Implementation Phases

### Phase 1: Chart Skeleton and Values (P1)

**Goal**: Create Chart.yaml, values.yaml, values-minikube.yaml, and _helpers.tpl.

**Steps**:
1. Create `helm/todo-app/Chart.yaml` (name: todo-app, version: 0.1.0, appVersion: 1.0.0).
2. Create `helm/todo-app/values.yaml` with:
   - backend/frontend image (repository, tag, pullPolicy)
   - replicas, resources (requests/limits)
   - env (DATABASE_URL, OPENAI_API_KEY, BETTER_AUTH_SECRET, NEXT_PUBLIC_API_URL) as placeholders or references
   - ingress enabled, host (e.g. todo.local)
3. Create `helm/todo-app/values-minikube.yaml`:
   - ingress host for Minikube (e.g. todo.minikube.local or minikube IP)
   - NEXT_PUBLIC_API_URL for frontend to reach backend (e.g. http://backend:8000 or Ingress URL)
4. Create `helm/todo-app/templates/_helpers.tpl` with:
   - `todo-app.labels` and common labels
   - `todo-app.backend.*` / `todo-app.frontend.*` helpers as needed

**Deliverables**: Chart.yaml, values.yaml, values-minikube.yaml, _helpers.tpl

**Verification**: `helm lint helm/todo-app` (may warn until templates exist).

---

### Phase 2: Backend and Frontend Deployments & Services (P1)

**Goal**: Add Deployment and Service templates for backend and frontend with health probes.

**Steps**:
1. Create `backend-deployment.yaml`:
   - image from values
   - env from ConfigMap/Secret
   - liveness: httpGet /health, port 8000
   - readiness: httpGet /ready, port 8000
   - securityContext runAsNonRoot if desired
2. Create `backend-service.yaml`: ClusterIP, port 8000, selector matching backend Deployment.
3. Create `frontend-deployment.yaml`:
   - image from values
   - env (NEXT_PUBLIC_API_URL from values)
   - liveness: httpGet /api/health, port 3000
   - securityContext runAsNonRoot if desired
4. Create `frontend-service.yaml`: ClusterIP, port 3000, selector matching frontend Deployment.

**Deliverables**: backend-deployment.yaml, backend-service.yaml, frontend-deployment.yaml, frontend-service.yaml

**Verification**: `helm template helm/todo-app` and ensure Deployments and Services render; `helm lint helm/todo-app`.

---

### Phase 3: ConfigMap, Secret, and Ingress (P2)

**Goal**: Add ConfigMap, Secret, and Ingress so the app can be configured and accessed in Minikube.

**Steps**:
1. Create `configmap.yaml`: Non-sensitive env (e.g. app name, log level) if any; or omit if all from values/Secret.
2. Create `secret.yaml`: Reference existingSecret name from values, OR use placeholder keys (e.g. database-url, better-auth-secret, openai-api-key) with values from `helm install --set` or a secret values file (not committed). Do not store real secrets in repo.
3. Create `ingress.yaml`: Conditional on `ingress.enabled`. Backend path (e.g. /api) -> backend service:8000; frontend path (/) -> frontend service:3000. Host from values.

**Deliverables**: configmap.yaml, secret.yaml, ingress.yaml

**Verification**: `helm template helm/todo-app -f helm/todo-app/values-minikube.yaml`; `helm lint helm/todo-app`.

---

### Phase 4: Validation and Documentation (P2)

**Goal**: Ensure chart passes lint, template renders, and README/docs mention Helm.

**Steps**:
1. Run `helm lint helm/todo-app` and fix any errors.
2. Run `helm template helm/todo-app` and `helm template helm/todo-app -f helm/todo-app/values-minikube.yaml`; confirm no template errors.
3. Add brief Helm section to root README (or link to 003) with: helm lint, helm template, and that 003 uses this chart for Minikube deploy.

**Deliverables**: Chart that lints and templates; optional README update.

---

## Technical Decisions

### TD-001: Single Chart vs Subcharts
**Decision**: Single chart `todo-app` with backend and frontend in one chart.
**Rationale**: Simpler for Minikube; single release; matches constitution “Helm charts for all services” (one chart for the app).

### TD-002: Secret Management
**Decision**: Secret template uses values (e.g. existingSecret name or keys from values). Real secret data provided at install time via `--set` or file (gitignored).
**Rationale**: No secrets in repo; aligns with Constitution (Secrets via K8s Secrets).

### TD-003: Ingress for Minikube
**Decision**: Ingress template with path-based routing: / -> frontend, /api -> backend. Host configurable via values-minikube.yaml.
**Rationale**: Single entrypoint for local dev; Minikube ingress addon can expose host.

### TD-004: Image Names
**Decision**: values.yaml uses image names compatible with 001 (e.g. todo-backend, todo-frontend) with tag default (e.g. latest or 0.1.0). User can override for local build.
**Rationale**: 003 will build images and load into Minikube; chart should work with those names.

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Helm template syntax error | High | helm lint and helm template in CI or pre-commit |
| Wrong probe paths | Medium | Use same paths as 001 (/health, /ready, /api/health) |
| Secret in repo by mistake | High | Secret template only refs; document “no real secrets in values” |

---

## Dependencies

### Internal
- 001-containerization complete (images build and health endpoints exist).

### External
- Helm 3 CLI.
- kubectl (optional, for 003).

---

## Estimated Effort

| Phase | Tasks | Estimated Time |
|-------|-------|----------------|
| Phase 1: Chart skeleton | 4 | 1 hour |
| Phase 2: Deployments & Services | 4 | 1–2 hours |
| Phase 3: ConfigMap, Secret, Ingress | 3 | 1 hour |
| Phase 4: Validation & docs | 2 | 0.5 hour |
| **Total** | **13** | **3.5–4.5 hours** |

---

## Next Steps

1. Run `/sp.tasks` (or hand-author) tasks.md from this plan.
2. Implement using `/sp.container-orchestration` and `/sp.devops-engineer` as appropriate.
3. Verify with helm lint and helm template.
4. Proceed to 003-minikube-deployment for actual Minikube deploy.

---

## Related Documents

- [Spec](./spec.md)
- [Phase 4 Overview](../overview.md)
- [001-containerization](../001-containerization/spec.md)
- [Constitution](../../../.specify/memory/constitution.md)
