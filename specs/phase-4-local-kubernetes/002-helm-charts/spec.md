# Feature Specification: Helm Charts

**Feature Branch**: `phase4-002-helm-charts`
**Created**: 2026-02-06
**Status**: Draft
**Phase**: 4 - Local Kubernetes Deployment
**Parent**: [Phase 4 Overview](../overview.md)

## Scope Statement

**This feature is INFRASTRUCTURE ONLY. No application code changes.**

### In Scope
- ✅ Helm chart for Todo Chatbot (single chart: frontend + backend)
- ✅ Chart metadata (Chart.yaml), default values (values.yaml)
- ✅ Minikube-specific values (values-minikube.yaml)
- ✅ Deployment templates for frontend and backend
- ✅ Service templates (ClusterIP) for frontend and backend
- ✅ Ingress template for local access
- ✅ ConfigMap and Secret templates for configuration
- ✅ Liveness and readiness probes using existing health endpoints
- ✅ Chart validation via `helm lint`

### Out of Scope
- ❌ NO changes to application code
- ❌ NO changes to Dockerfiles or docker-compose
- ❌ NO Minikube cluster creation or deployment (Feature 003)
- ❌ NO CI/CD or automation (Feature 003 scripts only)

---

## User Scenarios & Testing

### User Story 1 - Developer Creates Helm Chart Structure (Priority: P1)

As a developer, I want a Helm chart that packages frontend and backend so that I can deploy the Todo Chatbot to any Kubernetes cluster with a single command.

**Acceptance Scenarios**:

1. **Given** the chart exists at `helm/todo-app/`, **When** I run `helm lint helm/todo-app`, **Then** the chart passes validation with no errors.

2. **Given** the chart exists, **When** I run `helm template helm/todo-app`, **Then** valid Kubernetes manifests are generated for all resources.

3. **Given** the chart, **When** I run `helm template helm/todo-app -f helm/todo-app/values-minikube.yaml`, **Then** Minikube-specific values are applied correctly.

---

### User Story 2 - Developer Configures Deployments with Probes (Priority: P1)

As a developer, I want Deployments to include liveness and readiness probes so that Kubernetes can manage pod health correctly.

**Acceptance Scenarios**:

1. **Given** the backend Deployment template, **When** rendered, **Then** it includes liveness probe on `GET /health` and readiness probe on `GET /ready`.

2. **Given** the frontend Deployment template, **When** rendered, **Then** it includes liveness probe on `GET /api/health`.

3. **Given** both Deployments, **When** rendered, **Then** they use non-root securityContext where applicable and reference the same image names as built in 001-containerization.

---

### User Story 3 - Developer Manages Secrets and Config via Chart (Priority: P2)

As a developer, I want sensitive data (DATABASE_URL, API keys, auth secret) to be supplied via Kubernetes Secrets and non-sensitive config via ConfigMap or values so that I never hardcode secrets.

**Acceptance Scenarios**:

1. **Given** the chart, **When** I install with `helm install`, **Then** I can provide secrets via `--set` or a values file and they are mounted/used by the pods.

2. **Given** the Secret template, **When** rendered, **Then** it references placeholders or values (not literal secrets in repo).

3. **Given** the chart, **When** used with values-minikube.yaml, **Then** frontend receives correct backend URL for Minikube (e.g. via Ingress host or service name).

---

## Requirements

### Functional Requirements

#### Chart Structure
- **FR-001**: Chart MUST be located at `helm/todo-app/`
- **FR-002**: Chart MUST include Chart.yaml with name, version, appVersion
- **FR-003**: Chart MUST include values.yaml (defaults) and values-minikube.yaml (Minikube overrides)
- **FR-004**: Chart MUST pass `helm lint helm/todo-app` with no errors

#### Templates
- **FR-005**: Chart MUST have Deployment templates for backend and frontend
- **FR-006**: Chart MUST have Service templates (ClusterIP) for backend and frontend
- **FR-007**: Chart MUST have Ingress template for local access (Minikube)
- **FR-008**: Chart MUST have ConfigMap and/or Secret template for env configuration
- **FR-009**: Chart MUST include _helpers.tpl for shared labels and names

#### Probes
- **FR-010**: Backend Deployment MUST have liveness (path /health) and readiness (path /ready)
- **FR-011**: Frontend Deployment MUST have liveness (path /api/health)
- **FR-012**: Probes MUST use httpGet and appropriate initialDelaySeconds/periodSeconds

#### Values
- **FR-013**: values.yaml MUST allow overriding image repository and tag for backend and frontend
- **FR-014**: values.yaml MUST allow configuring replicas, resources (requests/limits)
- **FR-015**: values-minikube.yaml MUST set ingress host and any Minikube-specific settings
- **FR-016**: Secrets MUST be injectable via values (e.g. existingSecret name or key references), not stored in repo

### Non-Functional Requirements

- **NFR-001**: Chart MUST support Helm 3
- **NFR-002**: Rendered manifests MUST be valid for Kubernetes 1.24+
- **NFR-003**: No application logic or code changes

---

## Key Entities

### Chart Layout

```
helm/todo-app/
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

### Resource Summary

| Resource       | Backend | Frontend |
|----------------|---------|----------|
| Deployment     | ✅      | ✅       |
| Service        | ✅ ClusterIP | ✅ ClusterIP |
| Ingress        | ✅ (path /api) | ✅ (path /) |
| ConfigMap      | Optional / shared | Optional / shared |
| Secret         | ✅ (DB, auth, API keys) | ✅ (if needed) |
| Liveness       | /health | /api/health |
| Readiness      | /ready  | -        |

---

## Success Criteria

- **SC-001**: `helm lint helm/todo-app` passes
- **SC-002**: `helm template helm/todo-app` produces valid YAML for all listed resources
- **SC-003**: values-minikube.yaml is present and used for Minikube-specific config
- **SC-004**: No application source code or Dockerfiles modified
- **SC-005**: Deployments reference images compatible with 001-containerization (e.g. todo-backend, todo-frontend)

---

## Files to Create

| File | Action | Description |
|------|--------|-------------|
| `helm/todo-app/Chart.yaml` | CREATE | Chart metadata |
| `helm/todo-app/values.yaml` | CREATE | Default values |
| `helm/todo-app/values-minikube.yaml` | CREATE | Minikube overrides |
| `helm/todo-app/templates/_helpers.tpl` | CREATE | Shared template helpers |
| `helm/todo-app/templates/backend-deployment.yaml` | CREATE | Backend Deployment |
| `helm/todo-app/templates/backend-service.yaml` | CREATE | Backend Service |
| `helm/todo-app/templates/frontend-deployment.yaml` | CREATE | Frontend Deployment |
| `helm/todo-app/templates/frontend-service.yaml` | CREATE | Frontend Service |
| `helm/todo-app/templates/ingress.yaml` | CREATE | Ingress (optional/conditional) |
| `helm/todo-app/templates/configmap.yaml` | CREATE | ConfigMap for non-secret env |
| `helm/todo-app/templates/secret.yaml` | CREATE | Secret (placeholder / external ref) |

---

## Related Documents

- [Phase 4 Overview](../overview.md)
- [001-containerization spec](../001-containerization/spec.md) (prerequisite)
- [Constitution - Principle IX: Helm-Based Package Management](../../../.specify/memory/constitution.md)
- [003-minikube-deployment spec](../003-minikube-deployment/spec.md) (next feature)
