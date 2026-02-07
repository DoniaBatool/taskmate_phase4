# Tasks: Containerization

**Input**: Design documents from `specs/phase-4-local-kubernetes/001-containerization/`
**Prerequisites**: spec.md ✅, plan.md ✅
**Branch**: `phase4-001-containerization`

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Exact file paths included in descriptions

## Path Conventions

- **Backend**: `backend/`
- **Frontend**: `frontend/`
- **Docker**: `docker/`

---

## Phase 1: Backend Containerization (US1) 🎯 MVP

**Goal**: Create production-ready Docker image for FastAPI backend

**Independent Test**: `docker build ./backend && docker run -p 8000:8000 todo-backend && curl localhost:8000/health`

### Implementation for User Story 1

- [x] T001 [P] [US1] Create `.dockerignore` file in `backend/.dockerignore`
- [x] T002 [US1] Create multi-stage `Dockerfile` in `backend/Dockerfile`
- [x] T003 [US1] Add `/health` endpoint to `backend/src/main.py`
- [x] T004 [US1] Add `/ready` endpoint to `backend/src/main.py`
- [x] T005 [US1] Test: Build backend image and verify size < 500MB
- [x] T006 [US1] Test: Run backend container and verify `/health` returns 200

**Checkpoint**: Backend container builds and health endpoints work

---

## Phase 2: Frontend Containerization (US2)

**Goal**: Create production-ready Docker image for Next.js frontend

**Independent Test**: `docker build ./frontend && docker run -p 3000:3000 todo-frontend && curl localhost:3000/api/health`

### Implementation for User Story 2

- [x] T007 [P] [US2] Create `.dockerignore` file in `frontend/.dockerignore`
- [x] T008 [US2] Create multi-stage `Dockerfile` in `frontend/Dockerfile`
- [x] T009 [US2] Add health endpoint at `frontend/app/api/health/route.ts` (or pages/api/)
- [x] T010 [US2] Update `frontend/next.config.js` for standalone output
- [x] T011 [US2] Test: Build frontend image and verify size < 500MB
- [x] T012 [US2] Test: Run frontend container and verify `/api/health` returns 200

**Checkpoint**: Frontend container builds and health endpoint works

---

## Phase 3: Docker Compose Setup (US3)

**Goal**: Create Docker Compose for running full stack locally

**Independent Test**: `cd docker && docker-compose up && curl localhost:3000 && curl localhost:8000/health`

### Implementation for User Story 3

- [x] T013 [US3] Create `docker/` directory structure
- [x] T014 [US3] Create `docker/docker-compose.yml` with both services
- [x] T015 [P] [US3] Create `docker/docker-compose.dev.yml` for development overrides
- [ ] T016 [P] [US3] Create `docker/.env.example` with all required env vars
- [x] T017 [US3] Test: Run `docker-compose up` and verify both services start
- [x] T018 [US3] Test: Verify frontend can communicate with backend

**Checkpoint**: Full stack runs with Docker Compose

---

## Phase 4: Validation & Final Testing

**Goal**: Verify everything works correctly, no functionality changes

### Validation Tasks

- [x] T019 [P] Verify backend image size < 500MB: `docker images todo-backend`
- [x] T020 [P] Verify frontend image size < 500MB: `docker images todo-frontend`
- [x] T021 [P] Verify containers run as non-root: `docker exec <container> whoami`
- [x] T022 Test AI chatbot works in containerized environment
- [x] T023 Test all MCP tools work (add, list, update, delete, complete tasks)
- [x] T024 Update `README.md` with Docker setup instructions

**Checkpoint**: All validation passes, feature complete

---

## Task Details

### T001: Backend .dockerignore

**File**: `backend/.dockerignore`

```text
# Git
.git
.gitignore

# Python
__pycache__
*.py[cod]
*$py.class
*.so
.Python
.venv
venv/
ENV/
.pytest_cache/
.coverage
htmlcov/
.tox/
.mypy_cache/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
.env.*
!.env.example

# Tests
tests/
*_test.py
test_*.py

# Documentation
docs/
*.md
!README.md

# Docker
Dockerfile
.dockerignore
docker-compose*.yml
```

---

### T002: Backend Dockerfile

**File**: `backend/Dockerfile`

See plan.md for full Dockerfile specification.

Key requirements:
- Multi-stage build (builder → production)
- Base image: `python:3.13-slim`
- Non-root user: `appuser` (UID 1000)
- Expose port 8000
- HEALTHCHECK instruction

---

### T003: Backend /health endpoint

**File**: `backend/src/main.py`

Add to existing FastAPI app:

```python
@app.get("/health")
async def health_check():
    """Liveness probe - is the service running?"""
    return {"status": "healthy"}
```

---

### T004: Backend /ready endpoint

**File**: `backend/src/main.py`

Add to existing FastAPI app:

```python
from sqlalchemy import text

@app.get("/ready")
async def readiness_check():
    """Readiness probe - is the service ready to accept traffic?"""
    try:
        async with get_session() as session:
            await session.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database not ready: {str(e)}")
```

---

### T007: Frontend .dockerignore

**File**: `frontend/.dockerignore`

```text
# Git
.git
.gitignore

# Dependencies
node_modules

# Next.js
.next
out

# Environment
.env
.env.*
!.env.example

# IDE
.vscode/
.idea/
*.swp

# Tests
__tests__/
*.test.ts
*.test.tsx
*.spec.ts
*.spec.tsx
coverage/
.jest/

# Documentation
docs/
*.md
!README.md

# Docker
Dockerfile
.dockerignore
docker-compose*.yml

# Misc
.DS_Store
*.log
```

---

### T008: Frontend Dockerfile

**File**: `frontend/Dockerfile`

See plan.md for full Dockerfile specification.

Key requirements:
- Multi-stage build (deps → builder → production)
- Base image: `node:20-alpine`
- Non-root user: `appuser` (UID 1000)
- Standalone output mode
- Expose port 3000
- HEALTHCHECK instruction

---

### T009: Frontend Health Endpoint

**File**: `frontend/app/api/health/route.ts` (App Router)

```typescript
import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json({ status: 'healthy' })
}
```

OR if using Pages Router:

**File**: `frontend/pages/api/health.ts`

```typescript
import type { NextApiRequest, NextApiResponse } from 'next'

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  res.status(200).json({ status: 'healthy' })
}
```

---

### T010: Next.js Standalone Output

**File**: `frontend/next.config.js`

Add/update:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  // ... existing config
}

module.exports = nextConfig
```

---

### T014: Docker Compose

**File**: `docker/docker-compose.yml`

See plan.md for full docker-compose specification.

Key requirements:
- Backend service on port 8000
- Frontend service on port 3000
- Health checks for both services
- Environment variables from .env
- Service dependency (frontend depends on backend)

---

### T016: Environment Example

**File**: `docker/.env.example`

```bash
# =============================================================================
# Todo Chatbot - Docker Environment Variables
# =============================================================================
# Copy this file to .env and fill in the values
# cp .env.example .env
# =============================================================================

# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# Authentication
BETTER_AUTH_SECRET=your-secret-key-here

# OpenAI (for AI Chatbot)
OPENAI_API_KEY=sk-your-openai-api-key

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Backend)     Phase 2 (Frontend)
       ↓                     ↓
       └──────────┬──────────┘
                  ↓
           Phase 3 (Compose)
                  ↓
           Phase 4 (Validation)
```

### Task Dependencies

- **T001-T006**: Backend tasks (sequential within, parallel with T007-T012)
- **T007-T012**: Frontend tasks (sequential within, parallel with T001-T006)
- **T013-T018**: Docker Compose (requires T006 and T012 complete)
- **T019-T024**: Validation (requires T018 complete)

### Parallel Opportunities

```bash
# Phase 1 & 2 can run in parallel:
# Developer A: T001 → T002 → T003 → T004 → T005 → T006
# Developer B: T007 → T008 → T009 → T010 → T011 → T012

# Then sequential:
# T013 → T014 → T015 (parallel) + T016 (parallel) → T017 → T018
# T019 (parallel) + T020 (parallel) + T021 (parallel) → T022 → T023 → T024
```

---

## Verification Commands

### Backend Verification

```bash
# Build
docker build -t todo-backend:test ./backend

# Check size
docker images todo-backend:test --format "{{.Size}}"

# Run
docker run -d --name backend-test -p 8000:8000 \
  -e DATABASE_URL="$DATABASE_URL" \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  todo-backend:test

# Test health
curl http://localhost:8000/health
# Expected: {"status":"healthy"}

# Test ready
curl http://localhost:8000/ready
# Expected: {"status":"ready"}

# Check user
docker exec backend-test whoami
# Expected: appuser

# Cleanup
docker rm -f backend-test
```

### Frontend Verification

```bash
# Build
docker build -t todo-frontend:test ./frontend

# Check size
docker images todo-frontend:test --format "{{.Size}}"

# Run
docker run -d --name frontend-test -p 3000:3000 todo-frontend:test

# Test health
curl http://localhost:3000/api/health
# Expected: {"status":"healthy"}

# Check user
docker exec frontend-test whoami
# Expected: appuser

# Cleanup
docker rm -f frontend-test
```

### Docker Compose Verification

```bash
cd docker
cp .env.example .env
# Edit .env with real values

# Start
docker-compose up -d --build

# Check status
docker-compose ps

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:3000/api/health

# Test chatbot (manual)
# Open http://localhost:3000 and test AI chat

# Cleanup
docker-compose down
```

---

## Completion Checklist

Before marking feature complete:

- [ ] All 24 tasks completed
- [ ] Backend Dockerfile builds successfully
- [ ] Frontend Dockerfile builds successfully
- [ ] Backend image < 500MB
- [ ] Frontend image < 500MB
- [ ] Backend `/health` returns 200
- [ ] Backend `/ready` returns 200
- [ ] Frontend `/api/health` returns 200
- [ ] Docker Compose starts both services
- [ ] Services communicate correctly
- [ ] AI chatbot works in containers
- [ ] All MCP tools work
- [ ] Containers run as non-root
- [x] README updated with Docker instructions
- [ ] **No application logic changes** (except health endpoints)

---

## Notes

- [P] tasks = different files, no dependencies, can run parallel
- [Story] label maps task to user story for traceability
- Commit after each task or logical group
- Test each phase before moving to next
- **CRITICAL**: No changes to business logic, only infrastructure

---

## Post-Completion

After all tasks complete:
1. ✅ Run `/sp.skill-learner` to capture learnings
2. ✅ Create PHR for this feature
3. ✅ Move to next feature: `002-helm-charts`

