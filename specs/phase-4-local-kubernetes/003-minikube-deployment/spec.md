# Feature Specification: Minikube Deployment

**Feature Branch**: `phase4-003-minikube-deployment`
**Created**: 2026-02-06
**Status**: Draft
**Phase**: 4 - Local Kubernetes Deployment
**Parent**: [Phase 4 Overview](../overview.md)

## Scope Statement

**This feature is INFRASTRUCTURE ONLY. No application code changes.**

### In Scope
- ✅ Minikube cluster setup (start, addons: ingress, optional metrics-server)
- ✅ Build backend and frontend Docker images (from 001)
- ✅ Load images into Minikube (or build inside Minikube Docker env)
- ✅ Deploy using Helm chart from 002 with secrets supplied at install time
- ✅ Ingress accessible (host in /etc/hosts or minikube IP)
- ✅ Scripts: minikube setup, deploy (build + load + helm install)
- ✅ README section: Minikube setup and deploy instructions
- ✅ Verification: pods Running, health endpoints, app works (login, chat, MCP tools)
- ✅ Optional: Use kubectl-ai or Kagent for one operation (document in PHR)

### Out of Scope
- ❌ NO changes to application code
- ❌ NO changes to Helm chart (002) or Dockerfiles (001)
- ❌ NO cloud deployment (Phase V)
- ❌ NO CI/CD pipelines

---

## User Scenarios & Testing

### User Story 1 - Developer Starts Minikube and Deploys App (Priority: P1)

As a developer, I want to start a local Minikube cluster and deploy the Todo Chatbot using the Helm chart so that I can run the full app on Kubernetes locally.

**Acceptance Scenarios**:

1. **Given** Docker and Minikube are installed, **When** I run the Minikube setup script (or documented commands), **Then** Minikube starts with ingress addon enabled and cluster is ready.

2. **Given** the cluster is running, **When** I run the deploy script (or documented steps) with valid DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY, **Then** backend and frontend images are built/loaded and Helm installs the chart; all pods reach Running.

3. **Given** the release is installed, **When** I access the app via Ingress (e.g. http://todo.minikube.local or minikube IP), **Then** I see the Todo app UI and can sign in.

---

### User Story 2 - Developer Verifies App Behavior Unchanged (Priority: P1)

As a developer, I want to confirm that after deployment to Minikube the application behaves exactly as before (no functionality regression).

**Acceptance Scenarios**:

1. **Given** the app is deployed, **When** I open the frontend and sign in, **Then** I can create, list, update, delete, and complete tasks.

2. **Given** I am signed in, **When** I use the AI chat to say "Add a task to buy milk", **Then** the chatbot adds the task and responds correctly (MCP tools work).

3. **Given** the app is deployed, **When** I call GET /health and GET /ready on the backend (via Ingress or port-forward), **Then** I receive 200 with expected JSON.

---

### User Story 3 - Developer Uses AIOps (Optional, Priority: P2)

As a developer, I want to use kubectl-ai or Kagent for at least one operation so that AIOps is demonstrated as per Phase 4 requirements.

**Acceptance Scenarios**:

1. **Given** kubectl-ai or Kagent is installed, **When** I use it to e.g. check pod status, suggest a fix, or generate a manifest, **Then** the interaction is documented (e.g. in PHR or README).

2. **Alternative**: Document that AIOps was considered; if tools are not installed, document the intended usage for future.

---

## Requirements

### Functional Requirements

#### Minikube Setup
- **FR-001**: Documentation or script MUST start Minikube with at least 4 CPU and 8192 Mi memory (or document minimum).
- **FR-002**: Ingress addon MUST be enabled for Ingress resource to work.
- **FR-003**: Optional: metrics-server addon for resource visibility.

#### Build and Load Images
- **FR-004**: Backend image MUST be built from `backend/Dockerfile` and tagged for local use (e.g. todo-backend:latest).
- **FR-005**: Frontend image MUST be built from `frontend/Dockerfile` and tagged for local use (e.g. todo-frontend:latest).
- **FR-006**: Images MUST be available to Minikube (e.g. `minikube image load` or build inside `eval $(minikube docker-env)`).

#### Helm Deploy
- **FR-007**: Helm install MUST use chart at `helm/todo-app` with values from `values-minikube.yaml`.
- **FR-008**: Secrets (DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY) MUST be provided at install time via --set or a secret values file (not committed).
- **FR-009**: Release name MUST be consistent (e.g. todo-app) so that Ingress and resources are predictable.

#### Ingress Access
- **FR-010**: Ingress host (e.g. todo.minikube.local) MUST be reachable: either add /etc/hosts entry pointing to minikube IP, or use `minikube tunnel` / document browser access via minikube IP.
- **FR-011**: Frontend MUST receive correct NEXT_PUBLIC_API_URL so browser can call backend (e.g. http://todo.minikube.local/api or http://<minikube-ip>/api).

#### Verification
- **FR-012**: All pods (backend, frontend) MUST be in Running state before considering deploy successful.
- **FR-013**: Backend /health and /ready MUST return 200 when called (via Ingress or port-forward).
- **FR-014**: Frontend /api/health MUST return 200 when called.
- **FR-015**: User MUST be able to sign in, use tasks, and use AI chat with MCP tools (add, list, update, delete, complete).

### Non-Functional Requirements
- **NFR-001**: No application source code or business logic changes.
- **NFR-002**: Database remains external (Neon); no DB in cluster.
- **NFR-003**: Scripts and docs MUST be runnable on macOS (and ideally Linux).

---

## Key Entities

### Scripts (suggested)

| Script | Purpose |
|--------|---------|
| `scripts/minikube-setup.sh` | minikube start, addons enable |
| `scripts/deploy-minikube.sh` | Build images, load into Minikube, helm install with secrets |

### Documentation
- README: section "Minikube Deployment" with prerequisites, setup, deploy, access URL, and verification steps.
- Optional: `specs/phase-4-local-kubernetes/003-minikube-deployment/README.md` or VERIFY.md for step-by-step.

### Dependencies
- 001-containerization: Dockerfiles, images buildable
- 002-helm-charts: Chart at helm/todo-app, values-minikube.yaml
- External: Minikube, Helm, kubectl, Docker; Neon DB and OpenAI key for app to work

---

## Success Criteria

- **SC-001**: Minikube starts and ingress addon is enabled.
- **SC-002**: `helm install` (or upgrade) succeeds with chart + values-minikube + secrets.
- **SC-003**: All pods Running; backend and frontend health endpoints return 200.
- **SC-004**: App accessible via browser (Ingress host or minikube IP); user can log in and use tasks and AI chat.
- **SC-005**: No application code changes; Phase III behavior unchanged.
- **SC-006**: README includes Minikube setup and deploy instructions.

---

## Files to Create / Modify

| File | Action | Description |
|------|--------|-------------|
| `scripts/minikube-setup.sh` | CREATE | Start Minikube, enable addons |
| `scripts/deploy-minikube.sh` | CREATE | Build images, load, helm install |
| `README.md` | MODIFY | Add Minikube Deployment section |
| Optional: `003-minikube-deployment/VERIFY.md` | CREATE | Step-by-step verification |

---

## Related Documents

- [Phase 4 Overview](../overview.md)
- [001-containerization](../001-containerization/spec.md)
- [002-helm-charts](../002-helm-charts/spec.md)
- [Constitution - Kubernetes Deployment Requirements](../../../.specify/memory/constitution.md)
