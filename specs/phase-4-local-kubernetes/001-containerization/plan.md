# Implementation Plan: Containerization

**Branch**: `phase4-001-containerization` | **Date**: 2026-02-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/phase-4-local-kubernetes/001-containerization/spec.md`

## Summary

Containerize the existing Todo Chatbot application (frontend and backend) using Docker multi-stage builds. Create Docker Compose for local multi-container development. Add minimal health endpoints for container orchestration. **NO changes to application logic.**

## Technical Context

**Language/Version**: Python 3.13 (backend), Node.js 20 (frontend)
**Primary Dependencies**: FastAPI, Next.js 14, Docker, Docker Compose
**Storage**: Neon Serverless PostgreSQL (external - not containerized)
**Testing**: Manual container testing, health endpoint verification
**Target Platform**: Docker containers (linux/amd64, linux/arm64)
**Project Type**: Web application (monorepo)
**Performance Goals**: Image size < 500MB, startup < 30s
**Constraints**: No application code changes except health endpoints

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| VII. Container-First Deployment | ✅ Pass | Multi-stage builds, non-root user |
| I. Spec-Driven Development | ✅ Pass | Spec created before plan |
| VI. AI Chatbot Architecture | ✅ Protected | No changes to MCP tools or agent |
| V. Authentication & Security | ✅ Pass | Secrets via env vars, non-root containers |

## Project Structure

### Documentation (this feature)

```text
specs/phase-4-local-kubernetes/001-containerization/
├── spec.md              # Feature specification ✅
├── plan.md              # This file ✅
└── tasks.md             # To be created by /sp.tasks
```

### Source Code Changes

```text
backend/
├── Dockerfile           # NEW: Multi-stage production Dockerfile
├── .dockerignore        # NEW: Exclude unnecessary files
└── src/
    └── main.py          # MODIFY: Add /health and /ready endpoints

frontend/
├── Dockerfile           # NEW: Multi-stage production Dockerfile
├── .dockerignore        # NEW: Exclude unnecessary files
└── pages/api/           # Or app/api/ depending on structure
    └── health.ts        # NEW: Health check endpoint

docker/
├── docker-compose.yml       # NEW: Production compose
├── docker-compose.dev.yml   # NEW: Development overrides
└── .env.example             # NEW: Environment template
```

**Structure Decision**: Web application monorepo with separate frontend/backend directories. Docker configs in dedicated `docker/` directory.

## Implementation Phases

### Phase 1: Backend Containerization (P1)

**Goal**: Create production-ready Docker image for FastAPI backend

**Steps**:
1. Create `backend/.dockerignore`
2. Create `backend/Dockerfile` with multi-stage build
3. Add `/health` endpoint to `backend/src/main.py`
4. Add `/ready` endpoint to `backend/src/main.py`
5. Test: Build image and verify health endpoints

**Deliverables**:
- `backend/Dockerfile`
- `backend/.dockerignore`
- Health endpoints in `backend/src/main.py`

**Verification**:
```bash
docker build -t todo-backend:test ./backend
docker run -d -p 8000:8000 --name backend-test \
  -e DATABASE_URL="..." \
  -e OPENAI_API_KEY="..." \
  todo-backend:test
curl http://localhost:8000/health
# Expected: {"status": "healthy"}
docker rm -f backend-test
```

---

### Phase 2: Frontend Containerization (P1)

**Goal**: Create production-ready Docker image for Next.js frontend

**Steps**:
1. Create `frontend/.dockerignore`
2. Create `frontend/Dockerfile` with multi-stage build
3. Add `/api/health` endpoint to frontend
4. Test: Build image and verify health endpoint

**Deliverables**:
- `frontend/Dockerfile`
- `frontend/.dockerignore`
- Health endpoint in frontend

**Verification**:
```bash
docker build -t todo-frontend:test ./frontend
docker run -d -p 3000:3000 --name frontend-test todo-frontend:test
curl http://localhost:3000/api/health
# Expected: {"status": "healthy"}
docker rm -f frontend-test
```

---

### Phase 3: Docker Compose Setup (P2)

**Goal**: Create Docker Compose for running full stack locally

**Steps**:
1. Create `docker/` directory
2. Create `docker/docker-compose.yml`
3. Create `docker/docker-compose.dev.yml` (development overrides)
4. Create `docker/.env.example`
5. Test: Run full stack with `docker-compose up`

**Deliverables**:
- `docker/docker-compose.yml`
- `docker/docker-compose.dev.yml`
- `docker/.env.example`

**Verification**:
```bash
cd docker
cp .env.example .env
# Fill in .env with real values
docker-compose up --build
# Test frontend at http://localhost:3000
# Test backend at http://localhost:8000
# Test AI chatbot functionality
```

---

### Phase 4: Validation & Documentation

**Goal**: Verify everything works and document the setup

**Steps**:
1. Verify image sizes < 500MB
2. Verify containers run as non-root
3. Verify AI chatbot works in containers
4. Verify all MCP tools work
5. Update README with Docker instructions

**Verification Checklist**:
- [ ] Backend image < 500MB
- [ ] Frontend image < 500MB
- [ ] Containers run as non-root (UID 1000)
- [ ] Health endpoints respond correctly
- [ ] AI chatbot works
- [ ] All MCP tools work (add, list, update, delete, complete)
- [ ] No functionality changes from pre-container state

---

## Technical Decisions

### TD-001: Multi-Stage Builds
**Decision**: Use multi-stage Docker builds
**Rationale**: Reduces image size by excluding build tools from final image
**Alternative Rejected**: Single-stage build (larger image, security concerns)

### TD-002: Non-Root User
**Decision**: Run containers as non-root user (UID 1000)
**Rationale**: Security best practice, required for K8s security contexts
**Alternative Rejected**: Root user (security risk)

### TD-003: Alpine Base for Frontend
**Decision**: Use `node:20-alpine` for frontend
**Rationale**: Smaller image size (~150MB vs ~1GB for full node image)
**Alternative Rejected**: `node:20` (too large)

### TD-004: Slim Base for Backend
**Decision**: Use `python:3.13-slim` for backend
**Rationale**: Good balance of size and compatibility
**Alternative Rejected**: `python:3.13-alpine` (compatibility issues with some packages)

### TD-005: Health Check Strategy
**Decision**: Separate `/health` (liveness) and `/ready` (readiness) endpoints
**Rationale**: Kubernetes best practice - liveness checks if process is running, readiness checks if ready for traffic
**Alternative Rejected**: Single health endpoint (less granular control)

---

## Dockerfile Specifications

### Backend Dockerfile

```dockerfile
# =============================================================================
# Backend Dockerfile - Multi-Stage Build
# =============================================================================
# Stage 1: Builder - Install dependencies
# Stage 2: Production - Minimal runtime image
# =============================================================================

# Stage 1: Builder
FROM python:3.13-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml ./
COPY requirements.txt* ./

# Install dependencies
RUN uv pip install --system --no-cache -r requirements.txt || \
    uv pip install --system --no-cache .

# -----------------------------------------------------------------------------
# Stage 2: Production
FROM python:3.13-slim

WORKDIR /app

# Install runtime dependencies (curl for healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 -s /bin/bash appuser

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

```dockerfile
# =============================================================================
# Frontend Dockerfile - Multi-Stage Build
# =============================================================================
# Stage 1: Dependencies - Install npm packages
# Stage 2: Builder - Build Next.js application
# Stage 3: Production - Minimal runtime image
# =============================================================================

# Stage 1: Dependencies
FROM node:20-alpine AS deps

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci --only=production

# -----------------------------------------------------------------------------
# Stage 2: Builder
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Set environment for build
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

# Build application
RUN npm run build

# -----------------------------------------------------------------------------
# Stage 3: Production
FROM node:20-alpine

WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S -u 1000 -G nodejs appuser

# Set environment
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Copy necessary files from builder
COPY --from=builder --chown=appuser:nodejs /app/public ./public
COPY --from=builder --chown=appuser:nodejs /app/.next/standalone ./
COPY --from=builder --chown=appuser:nodejs /app/.next/static ./.next/static

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget -q --spider http://localhost:3000/api/health || exit 1

# Start application
CMD ["node", "server.js"]
```

### Docker Compose

```yaml
# =============================================================================
# Docker Compose - Todo Chatbot Phase 4
# =============================================================================
version: '3.8'

services:
  # ---------------------------------------------------------------------------
  # Backend Service (FastAPI)
  # ---------------------------------------------------------------------------
  backend:
    build:
      context: ../backend
      dockerfile: Dockerfile
    container_name: todo-backend
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
    restart: unless-stopped

  # ---------------------------------------------------------------------------
  # Frontend Service (Next.js)
  # ---------------------------------------------------------------------------
  frontend:
    build:
      context: ../frontend
      dockerfile: Dockerfile
    container_name: todo-frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      backend:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    restart: unless-stopped

# =============================================================================
# Networks
# =============================================================================
networks:
  default:
    name: todo-network
```

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Build fails on ARM64 (M1/M2 Mac) | Medium | Test on ARM64, use multi-platform build |
| Image size exceeds 500MB | Low | Use slim/alpine bases, multi-stage builds |
| Health endpoint breaks existing routes | Low | Use dedicated /health path, test thoroughly |
| Container can't connect to Neon DB | High | Test with real DB connection, document env vars |

---

## Dependencies

### External Dependencies
- Docker Desktop installed and running
- Network access to Neon PostgreSQL
- Valid OpenAI API key for chatbot testing

### Internal Dependencies
- Phase 3 application code must be stable
- No concurrent changes to backend/frontend during containerization

---

## Estimated Effort

| Phase | Tasks | Estimated Time |
|-------|-------|----------------|
| Phase 1: Backend | 5 tasks | 2-3 hours |
| Phase 2: Frontend | 4 tasks | 2-3 hours |
| Phase 3: Docker Compose | 5 tasks | 1-2 hours |
| Phase 4: Validation | 5 tasks | 1-2 hours |
| **Total** | **19 tasks** | **6-10 hours** |

---

## Next Steps

1. Run `/sp.tasks` to generate task list from this plan
2. Execute tasks using `/sp.implement`
3. Verify with checklist
4. Run `/sp.skill-learner` after completion

---

## Related Documents

- [Spec](./spec.md)
- [Phase 4 Overview](../overview.md)
- [Constitution](../../../.specify/memory/constitution.md)
