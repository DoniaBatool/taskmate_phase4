# Implementation Plan: Minikube Deployment

**Branch**: `phase4-003-minikube-deployment` | **Date**: 2026-02-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/phase-4-local-kubernetes/003-minikube-deployment/spec.md`

## Summary

Deploy the Todo Chatbot to a local Minikube cluster: start Minikube with ingress, build and load Docker images, install the Helm chart (002) with secrets, and verify the app is accessible and works (login, tasks, AI chat). **NO application code changes.**

## Technical Context

**Prerequisites**: 001-containerization (Dockerfiles, images buildable), 002-helm-charts (chart at helm/todo-app)
**Primary Dependencies**: Minikube, Docker, Helm, kubectl
**Target Platform**: Minikube (local Kubernetes)
**External**: Neon PostgreSQL (DATABASE_URL), OpenAI API key, Better Auth secret
**Constraints**: No application code or chart/Dockerfile changes

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| VII. Container-First Deployment | ✅ Pass | Use existing images from 001 |
| VIII. AIOps-Enabled K8s Operations | ✅ Pass | Optional kubectl-ai/Kagent use, document in PHR |
| IX. Helm-Based Package Management | ✅ Pass | Deploy via Helm chart from 002 |
| I. Spec-Driven Development | ✅ Pass | Spec before plan |
| VI. AI Chatbot Architecture | ✅ Protected | No app changes; verify chatbot works |

## Project Structure

### New / Modified

```text
scripts/
├── minikube-setup.sh      # CREATE: minikube start, addons
└── deploy-minikube.sh     # CREATE: build, load, helm install

README.md                  # MODIFY: Minikube Deployment section

specs/phase-4-local-kubernetes/003-minikube-deployment/
├── spec.md                # ✅
├── plan.md                # This file
├── tasks.md               # To be created
└── VERIFY.md              # Optional: step-by-step verify
```

**No changes** to `backend/`, `frontend/`, `docker/`, or `helm/todo-app/`.

## Implementation Phases

### Phase 1: Minikube Setup Script and Docs (P1)

**Goal**: Script and/or clear docs to start Minikube with required addons.

**Steps**:
1. Create `scripts/minikube-setup.sh` (or document equivalent commands):
   - `minikube start --cpus=4 --memory=8192 --driver=docker` (or document if different)
   - `minikube addons enable ingress`
   - Optional: `minikube addons enable metrics-server`
   - `kubectl get nodes` / `kubectl cluster-info` to verify
2. Script MUST be executable and idempotent where possible (e.g. minikube start is safe to re-run).
3. Document in README: prerequisite (Docker, Minikube, Helm, kubectl), and how to run the script.

**Deliverables**: `scripts/minikube-setup.sh`, README section "Minikube setup"

**Verification**: Run script on a machine with Minikube; cluster is ready, ingress addon enabled.

---

### Phase 2: Build Images and Load into Minikube (P1)

**Goal**: Backend and frontend images built and available inside Minikube.

**Steps**:
1. Document or script: build backend image (e.g. `docker build -t todo-backend:latest ./backend`).
2. Document or script: build frontend image (e.g. `docker build -t todo-frontend:latest ./frontend`).
3. Load into Minikube: either
   - `eval $(minikube docker-env)` then build (so images are in Minikube’s Docker), or
   - `minikube image load todo-backend:latest` and `minikube image load todo-frontend:latest`.
4. Ensure chart values (e.g. values-minikube) use image pull policy that uses local images (IfNotPresent) and correct tags.

**Deliverables**: Script or documented commands in deploy script / README

**Verification**: After running, `minikube image list` (or equivalent) shows todo-backend and todo-frontend.

---

### Phase 3: Helm Install with Secrets (P1)

**Goal**: Install Helm release with values-minikube and secrets; all pods Running.

**Steps**:
1. Create `scripts/deploy-minikube.sh` (or equivalent) that:
   - Optionally runs minikube-setup (or assumes cluster is up).
   - Builds and loads images (Phase 2).
   - Runs `helm upgrade --install todo-app helm/todo-app -f helm/todo-app/values-minikube.yaml` with secret values.
   - Secret values via `--set secret.databaseUrl=... --set secret.betterAuthSecret=... --set secret.openaiApiKey=...` or from a file (gitignored).
2. Document required env vars (DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY) and how to pass them (e.g. from .env or export).
3. Wait for pods: `kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=todo-app --timeout=120s` or document manual check.

**Deliverables**: `scripts/deploy-minikube.sh`, README "Deploy to Minikube" with helm install example

**Verification**: `kubectl get pods` shows backend and frontend pods Running; `kubectl get ingress` shows Ingress.

---

### Phase 4: Ingress Access and /etc/hosts (P2)

**Goal**: User can open app in browser via Ingress host.

**Steps**:
1. Document Ingress host (e.g. todo.minikube.local from values-minikube.yaml).
2. Document how to get Minikube IP: `minikube ip`.
3. Document adding to /etc/hosts: `<minikube-ip> todo.minikube.local` (or use minikube tunnel if preferred).
4. Optional: script that echoes the line to add to /etc/hosts.

**Deliverables**: README section "Access the app" with URL and /etc/hosts step

**Verification**: Opening http://todo.minikube.local (or http://<minikube-ip>) shows frontend; /api/health and backend /health work.

---

### Phase 5: Verification and AIOps (P2)

**Goal**: Verify app behavior; optionally use AIOps and document.

**Steps**:
1. Verification checklist in README or VERIFY.md:
   - Pods Running
   - Backend /health, /ready return 200
   - Frontend /api/health returns 200
   - Sign in, create/list/update/delete/complete tasks
   - AI chat: "Add a task to X" and confirm MCP tools work
2. Optional: Use kubectl-ai or Kagent once (e.g. "why is pod X not ready" or "list pods for todo-app") and document command and outcome in PHR or README.
3. README: "Minikube Deployment" section complete with setup, deploy, access, and verification.

**Deliverables**: README Minikube section complete; optional VERIFY.md; optional AIOps note in PHR

**Verification**: All checklist items pass; no app functionality regression.

---

## Technical Decisions

### TD-001: Image Loading Strategy
**Decision**: Prefer `eval $(minikube docker-env)` then build in repo, so images are in Minikube’s Docker daemon without separate load step. Alternative: build on host then `minikube image load`.
**Rationale**: Common pattern; avoids pushing to a registry for local dev.

### TD-002: Secret Handling in Script
**Decision**: Script accepts secrets via env vars (e.g. DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY) and passes to helm with --set, or reads from a .env file (gitignored). No secrets in repo.
**Rationale**: Matches constitution; same as 002.

### TD-003: Ingress Host
**Decision**: Use values-minikube host (e.g. todo.minikube.local). User adds /etc/hosts or uses minikube tunnel. Document both.
**Rationale**: Matches 002 chart; single place to change host.

### TD-004: Namespace
**Decision**: Deploy to default namespace unless we add namespace to chart later. Script and README use default.
**Rationale**: Simplicity for Phase 4; can add namespace in chart later if needed.

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Minikube resource limits (macOS) | Medium | Document 4 CPU, 8Gi memory; suggest closing other workloads |
| Ingress not working on Mac | Medium | Document minikube tunnel or NodePort fallback |
| Secret not set → pods fail | High | Script checks env vars and fails fast with clear message |
| DB/OpenAI unreachable from cluster | High | Document that Neon is external; network must allow cluster egress |

---

## Dependencies

### Internal
- 001-containerization complete (Dockerfiles, health endpoints).
- 002-helm-charts complete (helm/todo-app, values-minikube.yaml).

### External
- Docker Desktop (or Docker + Minikube driver).
- Minikube, Helm, kubectl.
- Neon DB URL, OpenAI API key, Better Auth secret.

---

## Estimated Effort

| Phase | Tasks | Estimated Time |
|-------|-------|----------------|
| Phase 1: Minikube setup script | 2–3 | 0.5 h |
| Phase 2: Build & load images | 2–3 | 0.5 h |
| Phase 3: Deploy script + helm install | 3–4 | 1 h |
| Phase 4: Ingress / hosts docs | 1–2 | 0.25 h |
| Phase 5: Verification + AIOps + README | 3–4 | 0.75 h |
| **Total** | **~14** | **~3 h** |

---

## Next Steps

1. Create tasks.md from this plan (or use /sp.tasks).
2. Implement scripts and README updates.
3. Run full flow: setup → deploy → access → verify.
4. Run /sp.skill-learner and create PHR after completion.

---

## Related Documents

- [Spec](./spec.md)
- [Phase 4 Overview](../overview.md)
- [002-helm-charts](../002-helm-charts/plan.md)
- [Constitution](../../../.specify/memory/constitution.md)
