# Phase 4: Local Kubernetes Deployment - Overview

**Phase**: 4 of 5
**Status**: In Progress
**Created**: 2026-02-06

## Phase Summary

Phase 4 focuses on **deploying the existing Todo Chatbot application to local Kubernetes (Minikube)** using containerization, Helm charts, and AIOps tools.

**CRITICAL: This is DEPLOYMENT ONLY. No changes to application features or business logic.**

## Scope Statement

### What Phase 4 DOES:
- ✅ Containerize existing frontend and backend (Dockerfiles)
- ✅ Create Docker Compose for local development
- ✅ Create Helm charts for Kubernetes deployment
- ✅ Deploy to local Minikube cluster
- ✅ Use AIOps tools (kubectl-ai, Kagent, Gordon)
- ✅ Configure health checks and probes
- ✅ Manage secrets via Kubernetes Secrets

### What Phase 4 DOES NOT DO:
- ❌ NO changes to API endpoints or routes
- ❌ NO changes to database models or schema
- ❌ NO changes to MCP tools or AI agent behavior
- ❌ NO changes to frontend components or UI
- ❌ NO changes to authentication or business logic
- ❌ NO new features
- ❌ NO cloud deployment (that's Phase V)

## Features Breakdown

| # | Feature | Description | Status | Spec |
|---|---------|-------------|--------|------|
| 001 | **Containerization** | Dockerfiles, docker-compose, .dockerignore | 🔄 In Progress | [spec.md](./001-containerization/spec.md) |
| 002 | **Helm Charts** | K8s package management, templates, values | 📋 Ready | [spec.md](./002-helm-charts/spec.md) |
| 003 | **Minikube Deployment** | Local K8s deploy, ingress, secrets | 📋 Ready | [spec.md](./003-minikube-deployment/spec.md) |

## Dependencies

### Prerequisites (Phase 1-3 Complete)
- ✅ Phase 1: Console app
- ✅ Phase 2: Full-stack web application (Next.js + FastAPI + Neon DB)
- ✅ Phase 3: AI Chatbot with MCP tools

### External Dependencies
- Docker Desktop installed
- Minikube installed
- Helm CLI installed
- kubectl installed
- kubectl-ai installed (optional, for AIOps)
- Kagent installed (optional, for AIOps)

### Feature Dependencies (Internal)
```
001-containerization
        ↓
002-helm-charts
        ↓
003-minikube-deployment
```

## Technology Stack

| Component | Technology |
|-----------|------------|
| Container Runtime | Docker (Docker Desktop) |
| Container Registry | Local (Minikube built-in) |
| Orchestration | Kubernetes (Minikube) |
| Package Manager | Helm Charts |
| AIOps Tools | kubectl-ai, Kagent, Gordon |

## Success Criteria

Phase 4 is complete when:
1. ✅ All Phase III functionality works unchanged
2. ✅ Frontend and backend containerized
3. ✅ Docker Compose works for local development
4. ✅ Helm charts created and validated
5. ✅ Application deployed to Minikube
6. ✅ All pods running with health checks
7. ✅ Application accessible via Ingress
8. ✅ AI chatbot works exactly as before
9. ✅ All MCP tools work exactly as before

## Timeline

| Feature | Estimated Duration |
|---------|-------------------|
| 001-containerization | 1-2 days |
| 002-helm-charts | 1-2 days |
| 003-minikube-deployment | 1 day |
| **Total** | **3-5 days** |

## Skills Used

| Feature | Primary Skills |
|---------|---------------|
| 001-containerization | `/sp.devops-engineer` |
| 002-helm-charts | `/sp.container-orchestration` |
| 003-minikube-deployment | `/sp.deployment-automation`, `/sp.container-orchestration` |

## Notes

- Database (Neon) remains external - not deployed to K8s
- Health endpoints may need to be added (minimal code change allowed)
- All secrets managed via K8s Secrets, not hardcoded
- Use AIOps tools where possible for manifest generation
