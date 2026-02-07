# Feature Specification: Containerization

**Feature Branch**: `phase4-001-containerization`
**Created**: 2026-02-06
**Status**: Draft
**Phase**: 4 - Local Kubernetes Deployment
**Parent**: [Phase 4 Overview](../overview.md)

## Scope Statement

**This feature is INFRASTRUCTURE ONLY. No application code changes except health endpoints.**

### In Scope
- ✅ Backend Dockerfile (multi-stage build)
- ✅ Frontend Dockerfile (multi-stage build)
- ✅ Docker Compose for local development
- ✅ .dockerignore files for both services
- ✅ Health check endpoints (minimal code addition)

### Out of Scope
- ❌ NO changes to API endpoints
- ❌ NO changes to database models
- ❌ NO changes to MCP tools
- ❌ NO changes to frontend components
- ❌ NO Kubernetes manifests (Feature 002)
- ❌ NO Helm charts (Feature 002)

---

## User Scenarios & Testing

### User Story 1 - Developer Builds Backend Container (Priority: P1)

As a developer, I want to build a production-ready Docker image for the backend so that I can deploy it to any container runtime.

**Why this priority**: Backend container is required before any Kubernetes deployment can happen.

**Independent Test**: Can be fully tested by running `docker build` and verifying the container starts and responds to health checks.

**Acceptance Scenarios**:

1. **Given** the backend source code exists, **When** I run `docker build -t todo-backend ./backend`, **Then** the image builds successfully without errors.

2. **Given** a built backend image, **When** I run the container with required env vars, **Then** the FastAPI server starts on port 8000.

3. **Given** a running backend container, **When** I call `GET /health`, **Then** I receive `{"status": "healthy"}` with HTTP 200.

4. **Given** a running backend container with DB connection, **When** I call `GET /ready`, **Then** I receive `{"status": "ready"}` with HTTP 200.

---

### User Story 2 - Developer Builds Frontend Container (Priority: P1)

As a developer, I want to build a production-ready Docker image for the frontend so that I can deploy it to any container runtime.

**Why this priority**: Frontend container is required before any Kubernetes deployment can happen.

**Independent Test**: Can be fully tested by running `docker build` and verifying the container starts and serves the Next.js app.

**Acceptance Scenarios**:

1. **Given** the frontend source code exists, **When** I run `docker build -t todo-frontend ./frontend`, **Then** the image builds successfully without errors.

2. **Given** a built frontend image, **When** I run the container, **Then** the Next.js server starts on port 3000.

3. **Given** a running frontend container, **When** I access the root URL, **Then** I see the Todo application UI.

4. **Given** a running frontend container, **When** I call `GET /api/health`, **Then** I receive `{"status": "healthy"}` with HTTP 200.

---

### User Story 3 - Developer Runs Full Stack Locally with Docker Compose (Priority: P2)

As a developer, I want to run both frontend and backend containers together using Docker Compose so that I can test the full application locally in containers.

**Why this priority**: Docker Compose enables local testing of containerized application before K8s deployment.

**Independent Test**: Can be tested by running `docker-compose up` and verifying both services work together.

**Acceptance Scenarios**:

1. **Given** Docker Compose file exists, **When** I run `docker-compose up`, **Then** both frontend and backend containers start successfully.

2. **Given** both containers are running, **When** I access the frontend, **Then** it can communicate with the backend API.

3. **Given** both containers are running, **When** I test the AI chatbot, **Then** it works exactly as before (no functionality changes).

4. **Given** both containers are running, **When** I create/list/update/delete tasks via chat, **Then** all MCP tools work correctly.

---

### Edge Cases

- What happens when DATABASE_URL is not set? → Container should fail fast with clear error
- What happens when OPENAI_API_KEY is missing? → Backend should start but chat endpoint returns error
- What happens when frontend can't reach backend? → Frontend shows connection error gracefully
- What happens when building on ARM64 (M1/M2 Mac)? → Images should build for correct architecture

---

## Requirements

### Functional Requirements

#### Backend Dockerfile
- **FR-001**: Dockerfile MUST use multi-stage build for optimized image size
- **FR-002**: Dockerfile MUST use `python:3.13-slim` as base image
- **FR-003**: Dockerfile MUST create non-root user `appuser` for security
- **FR-004**: Dockerfile MUST expose port 8000
- **FR-005**: Dockerfile MUST include HEALTHCHECK instruction
- **FR-006**: Final image MUST be less than 500MB

#### Frontend Dockerfile
- **FR-007**: Dockerfile MUST use multi-stage build for optimized image size
- **FR-008**: Dockerfile MUST use `node:20-alpine` as base image
- **FR-009**: Dockerfile MUST create non-root user `appuser` for security
- **FR-010**: Dockerfile MUST expose port 3000
- **FR-011**: Dockerfile MUST include HEALTHCHECK instruction
- **FR-012**: Final image MUST be less than 500MB

#### Docker Compose
- **FR-013**: Docker Compose MUST define both frontend and backend services
- **FR-014**: Docker Compose MUST configure proper networking between services
- **FR-015**: Docker Compose MUST support environment variables via .env file
- **FR-016**: Docker Compose MUST include health checks for both services
- **FR-017**: Docker Compose MUST map ports 3000 (frontend) and 8000 (backend)

#### .dockerignore Files
- **FR-018**: .dockerignore MUST exclude node_modules, __pycache__, .git
- **FR-019**: .dockerignore MUST exclude .env files (secrets)
- **FR-020**: .dockerignore MUST exclude test files and documentation

#### Health Endpoints
- **FR-021**: Backend MUST have `/health` endpoint returning `{"status": "healthy"}`
- **FR-022**: Backend MUST have `/ready` endpoint that checks database connectivity
- **FR-023**: Frontend MUST have `/api/health` endpoint returning `{"status": "healthy"}`

### Non-Functional Requirements

- **NFR-001**: Docker build time MUST be less than 5 minutes
- **NFR-002**: Container startup time MUST be less than 30 seconds
- **NFR-003**: Containers MUST run as non-root user
- **NFR-004**: Images MUST have no critical security vulnerabilities

---

## Key Entities

### Backend Dockerfile Structure
- **Stage 1 (builder)**: Install dependencies with UV
- **Stage 2 (production)**: Copy only necessary files, run as non-root

### Frontend Dockerfile Structure
- **Stage 1 (builder)**: Install dependencies, build Next.js
- **Stage 2 (production)**: Copy build artifacts, run as non-root

### Docker Compose Services
- **frontend**: Next.js application on port 3000
- **backend**: FastAPI application on port 8000

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: `docker build ./backend` completes successfully in under 5 minutes
- **SC-002**: `docker build ./frontend` completes successfully in under 5 minutes
- **SC-003**: Backend image size is less than 500MB
- **SC-004**: Frontend image size is less than 500MB
- **SC-005**: `docker-compose up` starts both services without errors
- **SC-006**: Health endpoints respond with 200 OK
- **SC-007**: AI chatbot works exactly as before in containerized environment
- **SC-008**: All MCP tools (add, list, update, delete, complete) work correctly

---

## Technical Specifications

### Backend Dockerfile

```dockerfile
# Stage 1: Builder
FROM python:3.13-slim AS builder
WORKDIR /app
COPY pyproject.toml .
RUN pip install uv && uv pip install --system -r pyproject.toml

# Stage 2: Production
FROM python:3.13-slim
WORKDIR /app

# Security: Non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Copy dependencies from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --chown=appuser:appuser . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

```dockerfile
# Stage 1: Builder
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-alpine
WORKDIR /app

# Security: Non-root user
RUN adduser -D -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

COPY --from=builder --chown=appuser:appuser /app/.next ./.next
COPY --from=builder --chown=appuser:appuser /app/public ./public
COPY --from=builder --chown=appuser:appuser /app/package*.json ./
COPY --from=builder --chown=appuser:appuser /app/node_modules ./node_modules

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget -q --spider http://localhost:3000/api/health || exit 1

CMD ["npm", "start"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      backend:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
```

### Health Endpoints

**Backend (add to src/main.py):**
```python
@app.get("/health")
async def health_check():
    """Liveness probe - is the service running?"""
    return {"status": "healthy"}

@app.get("/ready")
async def readiness_check():
    """Readiness probe - is the service ready to accept traffic?"""
    try:
        # Check database connectivity
        async with get_session() as session:
            await session.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database not ready: {str(e)}")
```

**Frontend (add pages/api/health.ts):**
```typescript
import { NextApiRequest, NextApiResponse } from 'next'

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  res.status(200).json({ status: 'healthy' })
}
```

---

## Files to Create/Modify

| File | Action | Description |
|------|--------|-------------|
| `backend/Dockerfile` | CREATE | Multi-stage production Dockerfile |
| `backend/.dockerignore` | CREATE | Exclude unnecessary files |
| `backend/src/main.py` | MODIFY | Add /health and /ready endpoints |
| `frontend/Dockerfile` | CREATE | Multi-stage production Dockerfile |
| `frontend/.dockerignore` | CREATE | Exclude unnecessary files |
| `frontend/pages/api/health.ts` | CREATE | Health check endpoint |
| `docker/docker-compose.yml` | CREATE | Multi-service compose file |
| `docker/docker-compose.dev.yml` | CREATE | Development overrides |

---

## Verification Checklist

Before marking this feature complete:

- [ ] Backend Dockerfile builds successfully
- [ ] Frontend Dockerfile builds successfully
- [ ] Backend image < 500MB
- [ ] Frontend image < 500MB
- [ ] Backend container starts and /health returns 200
- [ ] Frontend container starts and /api/health returns 200
- [ ] Docker Compose starts both services
- [ ] Services can communicate (frontend → backend)
- [ ] AI chatbot works in containerized environment
- [ ] All MCP tools work correctly
- [ ] No security vulnerabilities (docker scan)
- [ ] Containers run as non-root user

---

## Related Documents

- [Phase 4 Overview](../overview.md)
- [Constitution - Principle VII: Container-First Deployment](../../../.specify/memory/constitution.md)
- [002-helm-charts spec](../002-helm-charts/spec.md) (Next feature)
