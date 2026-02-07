<!--
  ==========================================================================
  SYNC IMPACT REPORT
  ==========================================================================
  Version Change: 6.1.0 → 6.2.0 (MINOR)
  Ratification Date: 2025-12-09
  Last Amended: 2026-02-06

  CHANGES IN THIS VERSION (6.2.0):

  Added/Modified Sections:
    - Skill Heading Display - MANDATORY before using any skill
    - Visual box format for skill start (╔══ USING SKILL ══╗)
    - Visual box format for skill complete (┌── SKILL COMPLETE ──┐)
    - Updated workflow diagram with visual skill headers
    - Added violation rule: "If skill NOT shown before use = VIOLATION"

  Key Changes:
    - Every skill usage MUST show visible heading BEFORE execution
    - User can see which skill is being used at all times
    - Clear visual distinction between skill start and completion

  Previous Changes (6.1.0):
    - AUTO SKILL LEARNING - MANDATORY (NON-NEGOTIABLE)
    - `/sp.skill-learner` is now AUTO-TRIGGERED (not manual)
    - Feature is NOT complete until skill-learner runs
    - All learnings MUST be captured and added to relevant skills

  Previous Changes (6.0.0):
    - Title: "Todo Hackathon Phase II" → "Todo Hackathon Phase IV"
    - Scope: Phase IV deployment-only scope (NO feature changes)
    - Principle VII: Container-First Deployment
    - Principle VIII: AIOps-Enabled Kubernetes Operations
    - Principle IX: Helm-Based Package Management
    - Phase IV Technology Stack, Requirements, Acceptance Criteria

  Templates Requiring Updates:
    ✅ plan-template.md - No changes needed (generic)
    ✅ spec-template.md - No changes needed (generic)
    ✅ tasks-template.md - No changes needed (generic)

  Follow-up TODOs:
    - None
  ==========================================================================
-->

# Todo Hackathon Phase IV Constitution
<!-- Local Kubernetes Deployment - Infrastructure Only -->

## ⚠️ CRITICAL SCOPE STATEMENT - PHASE IV

**Phase IV is DEPLOYMENT ONLY. NO changes to existing application features or business logic.**

### What Phase IV DOES:
- ✅ Containerize existing frontend and backend (Dockerfiles)
- ✅ Deploy to local Kubernetes (Minikube)
- ✅ Create Helm charts for package management
- ✅ Use AIOps tools (kubectl-ai, Kagent, Gordon) for deployment
- ✅ Configure health checks and probes
- ✅ Manage secrets via Kubernetes Secrets

### What Phase IV DOES NOT DO:
- ❌ NO changes to API endpoints or routes
- ❌ NO changes to database models or schema
- ❌ NO changes to MCP tools or AI agent behavior
- ❌ NO changes to frontend components or UI
- ❌ NO changes to authentication or business logic
- ❌ NO new features (that's Phase V with advanced features)
- ❌ NO cloud deployment (that's Phase V with DigitalOcean/GKE/AKS)

**The existing Phase III application MUST work exactly the same after containerization and K8s deployment. This is infrastructure work only.**

---

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
**All features must be specification-first:**
- Every feature starts with a complete specification document in `/specs` folder
- Specifications organized by type: features, api, database, ui
- Specifications must include user stories and acceptance criteria
- No code implementation without approved specification
- Claude Code must reference specifications during implementation
- Specs must be updated if requirements change
- Monorepo structure with layered CLAUDE.md files
- **Phase IV Addition**: K8s deployment specs in `/specs/kubernetes/`

### II. Full-Stack Code Quality Standards
**Code quality is mandatory across the stack:**

**Backend (Python/FastAPI):**
- Follow PEP 8 style guidelines strictly
- Type hints required for all function signatures
- Docstrings for all classes and public methods
- Maximum function length: 50 lines
- Single Responsibility Principle for all functions and classes

**Frontend (Next.js/TypeScript):**
- Follow TypeScript strict mode
- Use ESLint and Prettier configurations
- Server Components by default, Client Components only when needed
- Reusable component patterns
- Descriptive component and variable names

### III. Persistent Multi-User Storage
**Phase II requirement - database persistence:**
- All task data stored in Neon Serverless PostgreSQL
- SQLModel ORM for database operations
- User isolation - each user sees only their tasks
- Proper database migrations and schema management
- Connection pooling and efficient queries
- No hardcoded connection strings (use environment variables)
- **Phase IV**: Database remains external to K8s cluster (Neon Serverless)

### IV. RESTful API Architecture
**Backend API standards:**
- All routes under `/api/` prefix
- Consistent endpoint naming: `/api/{user_id}/tasks`
- Use proper HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Pydantic models for request/response validation
- Proper HTTP status codes (200, 201, 400, 401, 404, 500)
- JWT token authentication on all endpoints
- Comprehensive error handling with HTTPException

### V. Authentication & Security
**Multi-user security is mandatory:**
- Better Auth for user signup/signin
- JWT tokens for API authentication
- Shared secret between frontend and backend (BETTER_AUTH_SECRET)
- User ID verification on every API request
- Task ownership enforcement (users only access their data)
- Token expiry and refresh mechanism
- No exposed secrets in code (use .env files)
- **Phase IV**: Secrets managed via Kubernetes Secrets

### VI. AI Chatbot Architecture (Phase III - PROTECTED)
**Stateless AI-powered chatbot - NO CHANGES ALLOWED IN PHASE IV:**
- OpenAI Agents SDK for AI logic
- MCP (Model Context Protocol) tools for task operations
- Stateless chat endpoint with database-persisted conversation state
- Conversation/Message models in database
- Agent uses MCP tools to manage tasks
- Natural language task management
- All MCP tools: add_task, list_tasks, complete_task, update_task, delete_task

**⚠️ Phase IV MUST NOT modify any AI chatbot behavior or MCP tools.**

### VII. Container-First Deployment (NEW - Phase IV)
**All services MUST be containerized for deployment (infrastructure only):**
- Frontend and backend must have production-ready Dockerfiles
- Multi-stage builds for optimized image sizes
- Docker Compose for local multi-container development
- Container images must be scannable (no vulnerabilities P1/P2)
- Use Docker AI Agent (Gordon) for intelligent Docker operations when available
- Images tagged with git commit SHA for traceability

**Docker Requirements:**
- Base images: `python:3.13-slim` for backend, `node:20-alpine` for frontend
- Non-root users in production containers
- `.dockerignore` files to exclude unnecessary files
- Health check endpoints exposed
- NO application code changes - just packaging

### VIII. AIOps-Enabled Kubernetes Operations (NEW - Phase IV)
**AI-assisted Kubernetes operations are MANDATORY:**
- Use `kubectl-ai` for generating K8s manifests
- Use `Kagent` for cluster analysis and optimization
- Use Docker AI Agent (Gordon) for Docker operations (if available)
- AI-generated manifests must be reviewed before applying
- All AIOps interactions documented in PHR

**AIOps Tools:**
| Tool | Purpose | Usage |
|------|---------|-------|
| `kubectl-ai` | Generate K8s manifests, troubleshoot pods | `kubectl-ai "deploy frontend with 2 replicas"` |
| `Kagent` | Cluster analysis, resource optimization | `kagent "analyze cluster health"` |
| `Docker AI (Gordon)` | Docker operations (if available) | `docker ai "build optimized image"` |

### IX. Helm-Based Package Management (NEW - Phase IV)
**Helm charts for deployment management:**
- Helm charts must be created for all services
- Charts must support minikube environment
- Values files for environment-specific configuration
- Chart versioning aligned with application versions
- Use `kubectl-ai` or `Kagent` to generate initial charts

---

## Technology Stack Requirements

### Existing Technologies (Phase I-III - NO CHANGES)

**Frontend:**
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth with JWT

**Backend:**
- **Framework**: FastAPI
- **Language**: Python 3.13+
- **ORM**: SQLModel
- **Package Manager**: UV
- **AI Framework**: OpenAI Agents SDK
- **MCP**: Official MCP SDK

**Database:**
- **Service**: Neon Serverless PostgreSQL (EXTERNAL - not in K8s)
- **Schema Management**: SQLModel/Alembic migrations

### Phase IV Technologies (NEW - Deployment Only)

**Containerization:**
- **Container Runtime**: Docker (Docker Desktop)
- **Docker AI**: Docker AI Agent (Gordon) - if available
- **Compose**: Docker Compose for local development

**Orchestration:**
- **Local K8s**: Minikube
- **Package Manager**: Helm Charts
- **AI DevOps**: kubectl-ai, Kagent

---

## Phase IV Project Structure Additions

```
/
├── [EXISTING - NO CHANGES]
│   ├── frontend/           # Existing Next.js app
│   ├── backend/            # Existing FastAPI app
│   ├── specs/              # Existing specifications
│   └── ...
│
├── [NEW - Phase IV Additions]
│   ├── frontend/
│   │   ├── Dockerfile        # NEW: Production Dockerfile
│   │   └── .dockerignore     # NEW: Docker ignore file
│   ├── backend/
│   │   ├── Dockerfile        # NEW: Production Dockerfile
│   │   └── .dockerignore     # NEW: Docker ignore file
│   ├── docker/               # NEW: Docker configurations
│   │   ├── docker-compose.yml
│   │   ├── docker-compose.dev.yml
│   │   └── docker-compose.prod.yml
│   ├── helm/                 # NEW: Helm charts
│   │   └── todo-app/
│   │       ├── Chart.yaml
│   │       ├── values.yaml
│   │       ├── values-minikube.yaml
│   │       └── templates/
│   │           ├── _helpers.tpl
│   │           ├── frontend-deployment.yaml
│   │           ├── frontend-service.yaml
│   │           ├── backend-deployment.yaml
│   │           ├── backend-service.yaml
│   │           ├── ingress.yaml
│   │           ├── configmap.yaml
│   │           └── secret.yaml
│   ├── k8s/                  # NEW: Raw K8s manifests (optional)
│   │   ├── namespace.yaml
│   │   └── ...
│   ├── scripts/              # NEW: Deployment scripts
│   │   ├── minikube-setup.sh
│   │   ├── deploy-local.sh
│   │   └── helm-deploy.sh
│   └── specs/kubernetes/     # NEW: K8s deployment specs
│       └── local-deployment.md
```

---

## Docker Requirements

### Backend Dockerfile (Infrastructure Only)
```dockerfile
# Multi-stage build - NO application code changes
FROM python:3.13-slim AS builder
WORKDIR /app
COPY pyproject.toml .
RUN pip install uv && uv pip install --system .

FROM python:3.13-slim
WORKDIR /app
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY . .
EXPOSE 8000
HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile (Infrastructure Only)
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
RUN adduser -D appuser && chown -R appuser:appuser /app
USER appuser
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
HEALTHCHECK CMD wget -q --spider http://localhost:3000/api/health || exit 1
CMD ["npm", "start"]
```

---

## Kubernetes Deployment Requirements

### Minikube Setup
```bash
# Start Minikube with adequate resources
minikube start --cpus=4 --memory=8192 --driver=docker

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server

# Verify cluster health
kubectl get nodes
kubectl cluster-info
```

### Required K8s Resources

| Resource | Frontend | Backend |
|----------|----------|---------|
| Deployment | ✅ Required | ✅ Required |
| Service | ✅ ClusterIP | ✅ ClusterIP |
| Ingress | ✅ Path: / | ✅ Path: /api |
| ConfigMap | ✅ Env vars | ✅ Env vars |
| Secret | ✅ Auth secrets | ✅ DB + API secrets |
| Readiness Probe | ✅ Required | ✅ Required |
| Liveness Probe | ✅ Required | ✅ Required |

### Health Endpoints (Add to existing app - minimal change)

**Backend Health Endpoint** (add to existing main.py):
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/ready")
async def readiness_check(db: Session = Depends(get_session)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception:
        raise HTTPException(status_code=503, detail="Database not ready")
```

**Frontend Health Endpoint** (add if not exists):
```typescript
// pages/api/health.ts
export default function handler(req, res) {
  res.status(200).json({ status: 'healthy' })
}
```

---

## AIOps Integration

### kubectl-ai Usage Examples
```bash
# Generate deployment manifest
kubectl-ai "create deployment for todo-backend with 2 replicas"

# Troubleshoot failing pods
kubectl-ai "why is my todo-backend pod failing"

# Generate service manifest
kubectl-ai "create service for todo-backend on port 8000"
```

### Kagent Usage Examples
```bash
# Cluster health analysis
kagent "analyze my minikube cluster health"

# Resource optimization
kagent "check resource usage in todo-app namespace"
```

---

## Development Workflow - Phase IV

### Phase IV Workflow (Deployment Only)

1. **Containerization Phase**
   - Create Dockerfiles for frontend and backend
   - Test locally with Docker Compose
   - Verify existing functionality works in containers
   - **NO application code changes except health endpoints**

2. **Helm Chart Creation**
   - Use kubectl-ai/Kagent to generate initial manifests
   - Convert manifests to Helm charts
   - Create values files for minikube
   - Validate chart syntax with `helm lint`

3. **Minikube Deployment**
   - Start Minikube cluster
   - Deploy using Helm
   - Verify all pods running
   - Test Ingress access
   - **Verify app works exactly as before**

4. **Validation**
   - Test all existing functionality
   - Verify AI chatbot works
   - Verify all MCP tools work
   - **Ensure no functionality changes**

### Quality Gates - Phase IV

**Before considering Phase IV complete:**
- [ ] Frontend Dockerfile builds successfully
- [ ] Backend Dockerfile builds successfully
- [ ] Docker Compose works for local development
- [ ] Health endpoints implemented (minimal addition)
- [ ] Helm chart created with all templates
- [ ] Minikube deployment successful
- [ ] All pods in Running state
- [ ] Ingress configured and accessible
- [ ] Secrets managed via K8s Secrets
- [ ] **ALL existing functionality works unchanged**
- [ ] **AI chatbot works exactly as before**
- [ ] **All MCP tools work exactly as before**
- [ ] kubectl-ai or Kagent used for at least one operation
- [ ] README includes Minikube setup instructions

---

## Constraints & Non-Goals

### In Scope for Phase IV
- ✅ Containerization (Dockerfiles, docker-compose)
- ✅ Local Kubernetes deployment (Minikube)
- ✅ Helm charts for package management
- ✅ AIOps integration (kubectl-ai, Kagent)
- ✅ Health/readiness probes (minimal code addition)
- ✅ Ingress configuration
- ✅ K8s Secrets management
- ✅ Deployment scripts

### Out of Scope for Phase IV
- ❌ **NO changes to existing API endpoints**
- ❌ **NO changes to database models**
- ❌ **NO changes to MCP tools**
- ❌ **NO changes to AI agent behavior**
- ❌ **NO changes to frontend components**
- ❌ **NO new features**
- ❌ No cloud deployment (Phase V)
- ❌ No Kafka/event-driven architecture (Phase V)
- ❌ No Dapr integration (Phase V)
- ❌ No advanced features (Phase V)

---

## Phase IV Skills (Deployment-Focused)

### Required Skills for Phase IV

| Skill | When to Use | Output |
|-------|-------------|--------|
| `/sp.container-orchestration` | K8s deployment, Helm charts | K8s manifests, Helm charts |
| `/sp.devops-engineer` | Docker, deployment scripts | Dockerfiles, compose files |
| `/sp.deployment-automation` | Automated deployment | deploy.sh scripts |
| `/sp.production-checklist` | Deployment validation | Checklist report |

### Phase IV Skill Execution Plan

**Containerization:**
1. `/sp.devops-engineer` → Create Dockerfiles
2. `/sp.container-orchestration` → Validate container config
3. `/sp.production-checklist` → Check readiness

**Minikube Deployment:**
1. `/sp.container-orchestration` → Helm chart creation
2. `/sp.devops-engineer` → Minikube setup scripts
3. `/sp.deployment-automation` → Deploy scripts

---

## Phase IV Acceptance Criteria

**Phase IV is complete when:**

1. ✅ **All Phase III functionality works unchanged**
2. ✅ Frontend containerized with production Dockerfile
3. ✅ Backend containerized with production Dockerfile
4. ✅ Docker Compose works for local development
5. ✅ Health endpoints implemented
6. ✅ Helm chart created with all templates
7. ✅ Minikube cluster running with todo-app deployed
8. ✅ All pods in Running state
9. ✅ Ingress configured and accessible
10. ✅ Secrets managed via K8s Secrets
11. ✅ AIOps tools used (kubectl-ai or Kagent)
12. ✅ README includes Minikube setup instructions
13. ✅ **AI chatbot works exactly as before**
14. ✅ **All MCP tools work exactly as before**
15. ✅ **No business logic changes**

### Verification Tests

```bash
# After deployment, verify all existing functionality:
# 1. User can sign up/login
# 2. User can create tasks
# 3. User can list tasks
# 4. User can update tasks
# 5. User can delete tasks
# 6. User can complete tasks
# 7. AI chatbot responds to natural language
# 8. All MCP tools work via chat
```

---

## Phase III+ Requirements: Reusable Intelligence Skills (MANDATORY)

### ⚠️ CRITICAL ENFORCEMENT POLICY - SKILL-FIRST DEVELOPMENT

**THIS IS A NON-NEGOTIABLE REQUIREMENT FROM PROJECT TEACHERS/INSTRUCTORS**

The use of reusable intelligence skills is **MANDATORY** for ALL work. This is a religious enforcement policy.

### 🚨 ABSOLUTE REQUIREMENTS (MUST FOLLOW)

#### 1. Skills Are MANDATORY, Not Optional
- ✅ **REQUIRED**: Use existing skills for ALL implementation
- ❌ **VIOLATION**: Manual implementation when a skill exists
- ✅ **REQUIRED**: Create new skills for missing capabilities
- ❌ **VIOLATION**: Implementing without skill-based approach

#### 2. Terminal Output Is MANDATORY (RELIGIOUS ENFORCEMENT)

**BEFORE using ANY skill, Claude MUST show this heading:**

```text
╔══════════════════════════════════════════════════════════════╗
║  🔧 USING SKILL: /sp.skill-name                              ║
╠══════════════════════════════════════════════════════════════╣
║  Purpose: [What this skill does]                             ║
║  Constitution Check: ✓ Passed                                ║
╚══════════════════════════════════════════════════════════════╝
```

**AFTER skill completes, show:**

```text
┌──────────────────────────────────────────────────────────────┐
│  ✅ SKILL COMPLETE: /sp.skill-name                           │
├──────────────────────────────────────────────────────────────┤
│  Files Generated/Modified:                                   │
│    - path/to/file1                                           │
│    - path/to/file2                                           │
│  Time: [duration]                                            │
└──────────────────────────────────────────────────────────────┘
```

**If skill is NOT shown before use = VIOLATION**

#### 3. Skill Planning Is MANDATORY
Before implementing ANY work:
1. ✅ **STEP 1**: Analyze tasks
2. ✅ **STEP 2**: Map to existing skills
3. ✅ **STEP 3**: Display skill execution plan
4. ✅ **STEP 4**: Wait for user approval
5. ✅ **STEP 5**: Execute using skills
6. ✅ **STEP 6**: Report usage in PHR

---

### 📋 Skills Reference (44+ Available)

**Location**: All skills are in `.claude/skills/` directory

#### Phase IV Priority Skills

| Skill | When to Use | Output |
|-------|-------------|--------|
| `/sp.container-orchestration` | K8s deployment, Helm | K8s manifests, Helm charts |
| `/sp.devops-engineer` | Docker, deployment | Dockerfiles, scripts |
| `/sp.deployment-automation` | Automated deployment | deploy.sh scripts |
| `/sp.production-checklist` | Deployment validation | Checklist report |

#### Other Available Skills (Full List)

**Workflow & Planning (6):**
- `/sp.specify`, `/sp.plan`, `/sp.tasks`, `/sp.implement`, `/sp.new-feature`, `/sp.skill-learner`

**Core Implementation (6):**
- `/sp.mcp-tool-builder`, `/sp.ai-agent-setup`, `/sp.chatbot-endpoint`, `/sp.conversation-manager`, `/sp.database-schema-expander`, `/sp.robust-ai-assistant`

**Foundation (6):**
- `/sp.jwt-authentication`, `/sp.user-isolation`, `/sp.password-security`, `/sp.pydantic-validation`, `/sp.connection-pooling`, `/sp.transaction-management`

**Role-Based (7):**
- `/sp.backend-developer`, `/sp.frontend-developer`, `/sp.fullstack-architect`, `/sp.database-engineer`, `/sp.devops-engineer`, `/sp.security-engineer`, `/sp.uiux-designer`

**Quality & Testing (3):**
- `/sp.edge-case-tester`, `/sp.ab-testing`, `/sp.qa-engineer`

**Production & Deployment (5):**
- `/sp.performance-logger`, `/sp.structured-logging`, `/sp.deployment-automation`, `/sp.production-checklist`, `/sp.vercel-deployer`

**Modern Architecture (10):**
- `/sp.caching-strategy`, `/sp.api-contract-design`, `/sp.message-queue-integration`, `/sp.observability-apm`, `/sp.microservices-patterns`, `/sp.infrastructure-as-code`, `/sp.feature-flags-management`, `/sp.websocket-realtime`, `/sp.graphql-api`, `/sp.container-orchestration`

---

## 🧠 AUTO SKILL LEARNING - MANDATORY (NON-NEGOTIABLE)

### ⚠️ CRITICAL: Feature is NOT Complete Until Skill-Learner Runs

**This is RELIGIOUS enforcement. A feature is INCOMPLETE without skill learning.**

### Auto-Trigger Condition

`/sp.skill-learner` MUST be **AUTOMATICALLY** called when:
1. ✅ Feature implementation is complete
2. ✅ User has tested the feature and is satisfied
3. ✅ System tests have passed

**The system (Claude) MUST auto-invoke skill-learner without user asking for it.**

### Complete Feature Implementation Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: SKILL PLANNING (Before implementation)                 │
├─────────────────────────────────────────────────────────────────┤
│  📋 Feature: [Feature Name]                                     │
│  Skills Required: [List skills to use]                          │
│  Waiting for approval... ✋                                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: SKILL EXECUTION (During implementation)                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ╔═══════════════════════════════════════════════════════════╗  │
│  ║  🔧 USING SKILL: /sp.devops-engineer                      ║  │
│  ╠═══════════════════════════════════════════════════════════╣  │
│  ║  Purpose: Create Dockerfiles for containerization         ║  │
│  ║  Constitution Check: ✓ Passed                             ║  │
│  ╚═══════════════════════════════════════════════════════════╝  │
│                                                                 │
│  [... skill execution happens here ...]                         │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  ✅ SKILL COMPLETE: /sp.devops-engineer                   │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │  Files Generated:                                         │  │
│  │    - backend/Dockerfile                                   │  │
│  │    - frontend/Dockerfile                                  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ╔═══════════════════════════════════════════════════════════╗  │
│  ║  🔧 USING SKILL: /sp.container-orchestration              ║  │
│  ╠═══════════════════════════════════════════════════════════╣  │
│  ║  Purpose: Create Helm charts for K8s deployment           ║  │
│  ║  Constitution Check: ✓ Passed                             ║  │
│  ╚═══════════════════════════════════════════════════════════╝  │
│                                                                 │
│  [... next skill execution ...]                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: FEATURE TESTING                                        │
├─────────────────────────────────────────────────────────────────┤
│  🧪 Running tests...                                            │
│  ✅ All tests passed                                            │
│  👤 User verification: "Feature works correctly"                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: AUTO SKILL LEARNING (MANDATORY - AUTO-TRIGGERED)       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🧠 Skill Learning Session (AUTO-TRIGGERED)                     │
│                                                                 │
│  Feature Completed: [Feature Name]                              │
│  Skills Used:                                                   │
│    - /sp.skill-1                                                │
│    - /sp.skill-2                                                │
│                                                                 │
│  Analyzing learnings...                                         │
│                                                                 │
│  Learnings Captured:                                            │
│    ├── Bug Fix: [description] → Added to /sp.skill-1            │
│    ├── Pattern: [description] → Added to /sp.skill-2            │
│    ├── Edge Case: [description] → Added test to skill           │
│    └── Best Practice: [description] → Added checklist item      │
│                                                                 │
│  Skills Updated:                                                │
│    ✅ /sp.skill-1 (added bug fix pattern)                       │
│    ✅ /sp.skill-2 (added new pattern)                           │
│                                                                 │
│  🧠 Skills Evolution Complete                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  ✅ FEATURE FULLY COMPLETE                                      │
│  (Only after skill-learner has run)                             │
└─────────────────────────────────────────────────────────────────┘
```

### What Skill-Learner MUST Capture

After EVERY feature, skill-learner MUST analyze and capture:

| Category | Question | Action |
|----------|----------|--------|
| **Bug Fixes** | Did you fix any bugs during implementation? | Add solution pattern to relevant skill |
| **Edge Cases** | Did you discover edge cases not in skill? | Add test case to skill |
| **Patterns** | Did you discover a better approach? | Document pattern in skill |
| **Code Templates** | Did you write reusable code? | Add as template to skill |
| **Corrections** | Was original skill guidance wrong? | Correct the skill |
| **Checklists** | What steps should be remembered? | Add checklist items |

### Learning Categories Format

**Bug Fix Template:**
```markdown
### Issue: [Problem Title]
**Problem:** [What went wrong]
**Solution:** [How to fix it]
```python
# ❌ FAILS
[broken_code]

# ✅ WORKS
[fixed_code]
```
```

**Edge Case Template:**
```markdown
### Edge Case: [Scenario]
**When:** [Condition]
**Handle:** [How to handle]
**Test:**
```python
def test_edge_case():
    [test_code]
```
```

**Best Practice Template:**
```markdown
### Best Practice: [Title]
**Do:** [Correct approach]
**Don't:** [Wrong approach]
**Checklist:** [ ] [Action item]
```

### Skill Update Targets

Skills MUST be updated based on learnings:

| Skill Used | Update With |
|------------|-------------|
| `/sp.container-orchestration` | Dockerfile patterns, K8s issues, Helm tips |
| `/sp.devops-engineer` | Build issues, deployment fixes, script patterns |
| `/sp.deployment-automation` | CI/CD learnings, automation patterns |
| `/sp.mcp-tool-builder` | Tool parameter issues, error handling patterns |
| `/sp.chatbot-endpoint` | Conversation state issues, timeout handling |
| `/sp.robust-ai-assistant` | Date parsing, intent detection, fuzzy matching |

### Auto-Trigger Rules

**Claude MUST auto-invoke `/sp.skill-learner` when:**

1. **User says feature is working:**
   - "Chal gaya" / "It's working"
   - "Test kar liya" / "Tested it"
   - "Feature complete ho gaya"
   - "All good" / "Sab theek hai"

2. **Tests pass:**
   - All unit tests pass
   - Integration tests pass
   - Manual verification successful

3. **Implementation complete:**
   - All tasks in tasks.md marked done
   - No pending items

### VIOLATIONS (Feature Marked INCOMPLETE)

❌ **VIOLATION 1:** Not calling skill-learner after feature
```text
Claude: "Feature complete!"
[Does NOT call /sp.skill-learner]

❌ REJECTED - Feature is NOT complete
✅ CORRECT: Auto-invoke skill-learner after user confirms
```

❌ **VIOLATION 2:** User has to ask for skill-learner
```text
User: "Feature test ho gaya, skill-learner chala do"
Claude: [Runs skill-learner]

❌ PARTIAL - Should have been auto-triggered
✅ CORRECT: Auto-invoke without user asking
```

### Correct Flow Example

```text
User: "Containerization complete ho gayi, test kar liya, sab chal raha hai"

Claude:
  ✅ Feature verified as complete

  🧠 Skill Learning Session (AUTO-TRIGGERED)

  Feature: Phase IV Containerization
  Skills Used:
    - /sp.devops-engineer
    - /sp.container-orchestration
    - /sp.deployment-automation

  Analyzing learnings from implementation...

  Learnings Captured:
    ├── Issue: Multi-stage build COPY path was wrong
    │   → Added to /sp.devops-engineer
    ├── Pattern: Non-root user setup for both containers
    │   → Added template to /sp.container-orchestration
    ├── Edge Case: ARM64 vs AMD64 image compatibility
    │   → Added checklist to /sp.devops-engineer
    └── Best Practice: Use specific version tags not :latest
        → Added to /sp.container-orchestration

  Skills Updated:
    ✅ /sp.devops-engineer (3 additions)
    ✅ /sp.container-orchestration (2 additions)

  🧠 Skills Evolution Complete

  ✅ FEATURE FULLY COMPLETE
```

### PHR Documentation

Skill learning MUST be recorded in PHR:

```yaml
skill_learning:
  auto_triggered: true
  trigger_condition: "User confirmed feature working"
  feature: [Feature Name]
  skills_used:
    - /sp.skill-1
    - /sp.skill-2
  learnings_captured:
    - category: bug_fix
      description: [What was fixed]
      added_to: /sp.skill-1
    - category: pattern
      description: [Pattern discovered]
      added_to: /sp.skill-2
  skills_updated:
    - skill: /sp.skill-1
      additions: [Number]
    - skill: /sp.skill-2
      additions: [Number]
```

### Goal: Never Solve Same Problem Twice

**Once a problem is solved, it MUST live in a skill forever.**

- Every bug fixed → Added to skill
- Every pattern discovered → Added to skill
- Every edge case found → Added to skill
- Every workaround created → Added to skill

**Skills become smarter with every project. This is the LEARNING LOOP.**

---

## 🏭 Digital Agent Factory (17 FTE Agents)

### Phase IV Priority Agents

| Agent | Skills | Use For |
|-------|--------|---------|
| **devops-engineer** | 6 skills | Docker, K8s, Helm, deployment |
| **fullstack-architect** | 8 skills | Deployment architecture |
| **cloud-architect** | 7 skills | K8s resource planning |

### All Available Agents

**Orchestration (1):** orchestrator
**Backend (5):** backend-developer, database-engineer, security-engineer, qa-engineer, devops-engineer
**Frontend (3):** frontend-developer, uiux-designer, vercel-deployer
**Cross-Cutting (2):** fullstack-architect, github-specialist
**Enterprise (5):** data-engineer, technical-writer, cloud-architect, api-architect, product-manager

---

## Test-Driven Development (TDD) - Phase IV

### TDD for Containerization
1. **Write container tests first**
2. **Tests must FAIL** before implementation
3. **Implement** Dockerfiles
4. **Tests must PASS** after implementation

### Container Testing Script
```bash
#!/bin/bash
# tests/container_tests.sh

# Test: Docker build succeeds
docker build -t todo-backend:test ./backend || exit 1
docker build -t todo-frontend:test ./frontend || exit 1

# Test: Containers start and health check passes
docker run -d --name backend-test -p 8000:8000 todo-backend:test
sleep 10
curl -f http://localhost:8000/health || exit 1
docker rm -f backend-test

echo "Container tests passed!"
```

### K8s Testing Script
```bash
#!/bin/bash
# tests/k8s_tests.sh

# Test: Helm lint passes
helm lint ./helm/todo-app || exit 1

# Test: Pods are running
kubectl wait --for=condition=ready pod -l app=todo-app --timeout=120s || exit 1

echo "K8s tests passed!"
```

---

## Governance

### Constitution Authority
- This constitution supersedes all other development practices
- Phase IV is DEPLOYMENT ONLY - no feature changes allowed
- All changes must use skill-based approach
- Deviations require documented justification

### Amendment Procedure
1. Propose amendment with rationale
2. Review against project goals
3. Update constitution with proper versioning
4. Document in ADR if architecturally significant

### Version Policy
- **MAJOR**: Breaking changes to principles
- **MINOR**: New sections added
- **PATCH**: Clarifications, typo fixes

---

**Version**: 6.2.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2026-02-06 (Skill Heading Display - Mandatory Before Use)
