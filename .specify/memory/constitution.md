# Todo Hackathon Phase II Constitution      
<!-- Full-Stack Web Application with Persistent Storage -->

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

### VI. Core Feature Completeness
**All 5 Basic Level features are mandatory as web application:**
1. **Add Task**: Create new todo via REST API with title and description
2. **Delete Task**: Remove task by ID via REST API
3. **Update Task**: Modify existing task details via REST API
4. **View Task List**: Display all tasks via REST API with filtering
5. **Mark as Complete**: Toggle completion status via REST API

Each feature must work end-to-end: Frontend UI → API → Database

## Technology Stack Requirements

### Mandatory Technologies
**Frontend:**
- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth with JWT

**Backend:**
- **Framework**: FastAPI
- **Language**: Python 3.13+
- **ORM**: SQLModel
- **Package Manager**: UV

**Database:**
- **Service**: Neon Serverless PostgreSQL
- **Schema Management**: SQLModel migrations

**Development:**
- **AI Tool**: Claude Code with Spec-Kit Plus
- **Version Control**: Git with meaningful commit messages
- **Monorepo**: Single repository for frontend and backend

### Monorepo Project Structure
```
/
├── .specify/
│   ├── memory/
│   │   └── constitution.md
│   ├── templates/
│   └── scripts/
├── specs/
│   ├── overview.md
│   ├── architecture.md
│   ├── features/
│   │   ├── task-crud.md
│   │   └── authentication.md
│   ├── api/
│   │   └── rest-endpoints.md
│   ├── database/
│   │   └── schema.md
│   └── ui/
│       ├── components.md
│       └── pages.md
├── history/
│   ├── prompts/
│   └── adr/
├── frontend/
│   ├── CLAUDE.md
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── tasks/
│   ├── components/
│   ├── lib/
│   │   └── api.ts
│   ├── package.json
│   └── next.config.js
├── backend/
│   ├── CLAUDE.md
│   ├── main.py
│   ├── models.py
│   ├── routes/
│   │   └── tasks.py
│   ├── db.py
│   ├── auth.py
│   ├── pyproject.toml
│   └── tests/
├── docker-compose.yml
├── CLAUDE.md (root)
└── README.md
```

### Code Organization
**Backend Separation:**
- `models.py` - SQLModel database models (User, Task)
- `routes/` - API endpoint handlers
- `db.py` - Database connection and session management
- `auth.py` - JWT verification middleware
- `main.py` - FastAPI application entry point

**Frontend Separation:**
- `app/` - Next.js pages and layouts
- `components/` - Reusable React components
- `lib/api.ts` - API client with JWT token handling
- Server Components for static content
- Client Components for interactivity

## Development Workflow

### Specification Phase
1. Write feature specification in organized `/specs` structure:
   - `/specs/features/` - User stories and acceptance criteria
   - `/specs/api/` - REST endpoint specifications
   - `/specs/database/` - Schema and model definitions
   - `/specs/ui/` - Component and page specifications
2. Include user stories (As a user, I want...)
3. Define acceptance criteria (Given/When/Then)
4. Specify API contracts (request/response formats)
5. Get specification approved before coding

### Implementation Phase (Full-Stack)
1. Reference spec files with Claude Code:
   - `@specs/features/[feature].md` for feature requirements
   - `@specs/api/rest-endpoints.md` for API contracts
   - `@specs/database/schema.md` for database models
2. Implement backend first:
   - Database models (SQLModel)
   - API endpoints (FastAPI)
   - Authentication middleware
   - Write and run backend tests
3. Implement frontend:
   - API client configuration
   - React components
   - Page layouts and routing
   - Authentication flow
4. Test end-to-end workflow
5. Verify all acceptance criteria met

### Quality Gates
**Before considering a feature complete:**
- [ ] Specification documents exist (feature, api, database, ui)
- [ ] Backend API implemented and tested
- [ ] Frontend UI implemented and connected to API
- [ ] Authentication working correctly
- [ ] Database models created with proper relationships
- [ ] Code follows standards (PEP 8 for Python, ESLint for TypeScript)
- [ ] Type hints/types present in both frontend and backend
- [ ] Environment variables properly configured
- [ ] Manual end-to-end testing performed
- [ ] No bugs or edge cases remaining
- [ ] User can only access their own tasks

### Git Workflow
- Meaningful commit messages: `feat: add task creation API endpoint`
- Commit after each completed feature (backend + frontend)
- Keep commits atomic and focused
- Include spec files in repository
- Separate commits for backend and frontend when appropriate

## Constraints & Non-Goals

### In Scope for Phase II
- Basic task management as web application (add, delete, update, view, complete)
- Persistent storage in PostgreSQL database
- Multi-user support with authentication
- RESTful API architecture
- Responsive web interface
- Input validation and error handling
- User isolation and data security
- JWT-based authentication

### Out of Scope for Phase II
- ❌ No advanced features yet (priorities, tags, due dates, recurring tasks)
- ❌ No AI chatbot (Phase III)
- ❌ No Kubernetes deployment (Phase IV-V)
- ❌ No event-driven architecture (Phase V)
- ❌ No real-time sync across clients
- ❌ No file attachments or media
- ❌ No email notifications

### Database Schema Constraints

**users table (managed by Better Auth):**
- `id`: String (primary key, UUID)
- `email`: String (unique, required)
- `name`: String (optional)
- `created_at`: Timestamp (auto-generated)

**tasks table:**
- `id`: Integer (primary key, auto-incremented)
- `user_id`: String (foreign key → users.id, required)
- `title`: String (1-200 characters, required)
- `description`: Text (max 1000 characters, optional)
- `completed`: Boolean (default False)
- `created_at`: Timestamp (auto-generated)
- `updated_at`: Timestamp (auto-updated)

**Indexes:**
- `tasks.user_id` (for efficient filtering by user)
- `tasks.completed` (for status filtering)

## Error Handling Standards

### Backend API Error Handling
**HTTP Status Codes:**
- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST
- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Missing or invalid JWT token
- `403 Forbidden` - User doesn't own the resource
- `404 Not Found` - Task or user not found
- `500 Internal Server Error` - Unexpected server errors

**Error Response Format:**
```json
{
  "detail": "Clear error message",
  "error_code": "TASK_NOT_FOUND"
}
```

### Frontend Error Handling
- Display user-friendly error messages (not raw API errors)
- Show loading states during API calls
- Handle network failures gracefully
- Provide retry mechanisms for failed requests
- Toast notifications for success/error feedback
- Form validation before API submission

### Input Validation
**Backend (FastAPI Pydantic):**
- Title: 1-200 characters, required
- Description: max 1000 characters, optional
- User ID: valid UUID format
- Task ID: positive integer

**Frontend (Client-side):**
- Pre-validate forms before submission
- Show inline validation errors
- Disable submit button during processing
- Clear error messages for users

### Security Error Handling
- Never expose database errors to frontend
- Log detailed errors server-side only
- Use try-except blocks appropriately
- Never expose JWT secrets or connection strings
- Rate limiting on authentication endpoints

## API Endpoint Specifications

### Required REST API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks for authenticated user |
| POST | `/api/{user_id}/tasks` | Create a new task |
| GET | `/api/{user_id}/tasks/{id}` | Get specific task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle task completion |

### API Security Requirements
- All endpoints require `Authorization: Bearer <JWT_TOKEN>` header
- JWT token must be verified using BETTER_AUTH_SECRET
- User ID in URL must match authenticated user ID from token
- Return 401 if token missing or invalid
- Return 403 if user_id doesn't match token

### Request/Response Examples

**POST /api/{user_id}/tasks**
```json
Request: {
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
Response (201): {
  "id": 1,
  "user_id": "user-uuid",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-09T10:00:00Z",
  "updated_at": "2025-12-09T10:00:00Z"
}
```

## Governance

### Constitution Authority
- This constitution supersedes all other development practices
- All Claude Code interactions must reference and follow these principles
- Deviations require documented justification
- Root and layered CLAUDE.md files must reference this constitution
- Monorepo structure must be maintained

### Acceptance Criteria
**Phase II is complete when:**
1. ✅ All 5 Basic Level features implemented as web application
2. ✅ Backend API with all required endpoints functional
3. ✅ Frontend Next.js application with responsive UI
4. ✅ Better Auth authentication working (signup/signin)
5. ✅ JWT token verification on all API endpoints
6. ✅ User isolation enforced (users only see their tasks)
7. ✅ Neon PostgreSQL database connected and working
8. ✅ SQLModel models created with proper relationships
9. ✅ All tests passing (backend and frontend)
10. ✅ Code meets quality standards (PEP 8, ESLint)
11. ✅ Environment variables properly configured
12. ✅ README.md includes setup instructions for both frontend and backend
13. ✅ CLAUDE.md files at root, frontend, and backend levels
14. ✅ specs folder contains organized specifications (features, api, database, ui)
15. ✅ Application deployed to Vercel (frontend) and accessible via public URL

### Success Metrics
- ✅ Frontend and backend run without errors
- ✅ All CRUD operations functional via web interface
- ✅ Users can signup, signin, and manage only their tasks
- ✅ Authentication and authorization working correctly
- ✅ Database persistence working (data survives server restart)
- ✅ Responsive UI works on desktop and mobile
- ✅ Clean, maintainable monorepo codebase
- ✅ Complete documentation for both frontend and backend
- ✅ API endpoints follow REST conventions
- ✅ Ready for demo video (under 90 seconds)
- ✅ Deployed and accessible online

### Deployment Requirements
**Frontend (Vercel):**
- Environment variables: `BETTER_AUTH_SECRET`, `NEXT_PUBLIC_API_URL`
- Build succeeds without errors
- Public URL accessible

**Backend (Python hosting or containerized):**
- Environment variables: `DATABASE_URL`, `BETTER_AUTH_SECRET`
- FastAPI app runs and serves API requests
- Accessible from frontend (CORS configured)

**Database (Neon):**
- PostgreSQL database provisioned
- Tables created via SQLModel migrations
- Connection string secured in environment variables

## Phase III+ Requirements: Reusable Intelligence Skills (MANDATORY)

### ⚠️ CRITICAL ENFORCEMENT POLICY - SKILL-FIRST DEVELOPMENT

**THIS IS A NON-NEGOTIABLE REQUIREMENT FROM PROJECT TEACHERS/INSTRUCTORS**

Starting from Phase III (AI Chatbot) and all subsequent phases, the use of reusable intelligence skills is **MANDATORY** for ALL feature development. This is a religious enforcement policy.

### 🚨 ABSOLUTE REQUIREMENTS (MUST FOLLOW)

#### 1. Skills Are MANDATORY, Not Optional
- ✅ **REQUIRED**: Use existing skills for ALL feature implementation
- ❌ **VIOLATION**: Manual implementation when a skill exists
- ✅ **REQUIRED**: Create new skills for missing capabilities
- ❌ **VIOLATION**: Implementing features without skill-based approach

#### 2. Terminal Output Is MANDATORY
Every skill usage MUST produce visible terminal output:
```text
🔧 Using Skill: /sp.skill-name

Purpose: [What this skill does]
Constitution Check: ✓ Passed
Tasks Covered: T123-T125
Files Generated:
  - path/to/file1.py
  - path/to/file2.py
  - path/to/test.py

✅ Skill Complete
```

**If you don't see this output, the skill was NOT used (VIOLATION).**

#### 3. Skill Planning Is MANDATORY
Before implementing ANY feature:
1. ✅ **STEP 1**: Analyze all tasks in the feature
2. ✅ **STEP 2**: Map each task to existing skills OR identify need for new skills
3. ✅ **STEP 3**: Display skill execution plan in terminal
4. ✅ **STEP 4**: Wait for user approval
5. ✅ **STEP 5**: Execute using identified skills (invoke via Skill tool)
6. ✅ **STEP 6**: Report skill usage in PHR and commit message

**Example Terminal Output:**
```text
🔧 Phase 8: Performance Optimization

Skills Plan:
1. /sp.connection-pooling → Verify pool configuration (T163-T164)
2. /sp.skill-creator → Create /sp.performance-logger (T165-T166)
3. /sp.performance-logger → Add execution time logging
4. /sp.ab-testing → Run load tests (T167-T169)

Waiting for approval... ✋
```

#### 4. Skill Creation Is MANDATORY When Needed
If no skill exists for required capability:
1. ✅ Use `/sp.skill-creator` to create new skill FIRST
2. ✅ Document new skill in `SKILLS.md`
3. ✅ THEN use the newly created skill
4. ❌ NEVER implement manually if capability can be a skill

### 📋 Complete Skills Reference (31 Available Skills)

**Location**: All skills are in `.claude/skills/` directory
**Usage**: Invoke via `Skill` tool with skill name (e.g., `/sp.mcp-tool-builder`)
**Requirement**: MUST be used for ALL applicable work in Phase III+

---

#### 1️⃣ Workflow & Planning Skills (5 skills)

| Skill | When to Use | Auto-Trigger | Output |
|-------|-------------|--------------|--------|
| `/sp.specify` | Creating feature specifications | When user requests new feature | `specs/{feature}/spec.md` |
| `/sp.plan` | Generating implementation plans | After spec created | `specs/{feature}/plan.md` |
| `/sp.tasks` | Breaking down into tasks | After plan created | `specs/{feature}/tasks.md` |
| `/sp.implement` | Executing implementation | After tasks created | Code files, tests |
| `/sp.new-feature` | Complete spec→plan→tasks flow | User requests "new feature from scratch" | All three files in one workflow |

**When user says**: "Create a new feature for X" → Use `/sp.new-feature`
**When user says**: "Plan how to implement X" → Use `/sp.plan`

---

#### 2️⃣ Core Implementation Skills - Phase III (5 skills)

| Skill | When to Use | Tasks Covered | Constitution Principle |
|-------|-------------|---------------|----------------------|
| `/sp.mcp-tool-builder` | Creating MCP tools for AI agent | Task CRUD operations (add, list, update, delete, complete) | Principle VI (MCP-First Design) |
| `/sp.ai-agent-setup` | Configuring OpenAI Agents SDK | AI agent initialization, tool binding | Principle II (Stateless Architecture) |
| `/sp.chatbot-endpoint` | Creating stateless chat API | Chat endpoint with JWT validation | Principle II (Stateless), Principle V (Security) |
| `/sp.conversation-manager` | Managing conversation state | Conversation/Message models, history | Principle III (Database-Centric State) |
| `/sp.database-schema-expander` | Adding new database tables | New SQLModel models, migrations, indexes | Principle III (Database-Centric State) |

**When user says**: "Add chat functionality" → Use `/sp.ai-agent-setup` + `/sp.chatbot-endpoint` + `/sp.conversation-manager`
**When user says**: "Create add_task tool" → Use `/sp.mcp-tool-builder`

---

#### 3️⃣ Foundation Skills - Phase II Patterns (6 skills)

| Skill | When to Use | Tasks Covered | Constitution Principle |
|-------|-------------|---------------|----------------------|
| `/sp.jwt-authentication` | Setting up user authentication | JWT creation/verification, protected endpoints | Principle V (Security & User Isolation) |
| `/sp.user-isolation` | Protecting user-owned resources | Query scoping, ownership checks, security logging | Principle V (Security & User Isolation) |
| `/sp.password-security` | Implementing signup/login | bcrypt hashing, signup/login endpoints, secure schemas | Principle V (Security & User Isolation) |
| `/sp.pydantic-validation` | Creating API endpoints | Request/response DTOs, custom validators | Principle IV (RESTful API Architecture) |
| `/sp.connection-pooling` | Setting up database connections | Engine config, pool settings, health monitoring | Principle VII (Database Performance) |
| `/sp.transaction-management` | Implementing database writes | Try/commit/rollback, multi-step atomicity | Principle III (Database-Centric State) |

**When user says**: "Add authentication" → Use `/sp.jwt-authentication` + `/sp.password-security`
**When user says**: "Protect user data" → Use `/sp.user-isolation`

---

#### 4️⃣ Role-Based Development Skills (7 skills)

| Skill | When to Use | Capabilities | Best For |
|-------|-------------|--------------|----------|
| `/sp.backend-developer` | Backend API implementation | FastAPI endpoints, SQLModel, business logic | REST API, database operations |
| `/sp.frontend-developer` | Frontend UI implementation | Next.js, React components, API client | UI/UX, user interfaces |
| `/sp.fullstack-architect` | System design & architecture | End-to-end architecture, integration | Complex multi-layer features |
| `/sp.database-engineer` | Database optimization | Schema design, indexes, migrations, queries | Database performance, data modeling |
| `/sp.devops-engineer` | Infrastructure & deployment | Docker, CI/CD, environment setup | Deployment, infrastructure |
| `/sp.security-engineer` | Security hardening | OWASP audit, vulnerability scanning, security tests | Security compliance, penetration testing |
| `/sp.uiux-designer` | User experience design | Wireframes, user flows, component design | Design-first features |

**When user says**: "Implement backend API" → Use `/sp.backend-developer`
**When user says**: "Create UI for X" → Use `/sp.frontend-developer`
**When user says**: "Run security audit" → Use `/sp.security-engineer`

---

#### 5️⃣ Quality & Testing Skills (3 skills)

| Skill | When to Use | Test Coverage | Auto-Trigger |
|-------|-------------|---------------|--------------|
| `/sp.edge-case-tester` | After any feature implementation | 57+ edge case scenarios | ✅ Automatically after `/sp.implement` |
| `/sp.ab-testing` | Validating feature variations | A/B test framework, variant configs, analytics | Manual - for experiments |
| `/sp.qa-engineer` | Creating comprehensive test suites | Unit tests, integration tests, smoke tests, E2E | When implementing critical features |

**When user says**: "Test this feature" → Use `/sp.edge-case-tester` + `/sp.qa-engineer`
**When user says**: "Run A/B test" → Use `/sp.ab-testing`

---

#### 6️⃣ Production & Deployment Skills (5 skills)

| Skill | When to Use | Tasks Covered | Output |
|-------|-------------|---------------|--------|
| `/sp.performance-logger` | Adding performance monitoring | Execution time logging, structured metrics | `utils/performance.py`, decorators |
| `/sp.structured-logging` | Setting up production logging | JSON logging, log aggregation compatibility | `logging_config.py`, error context |
| `/sp.deployment-automation` | Creating deployment workflows | Deploy scripts, validation, health checks | `scripts/deploy.sh`, CI/CD configs |
| `/sp.production-checklist` | Validating production readiness | Security, performance, monitoring checklists | Production readiness report |
| `/sp.vercel-deployer` | Deploying to Vercel | Frontend deployment, environment config | Vercel deployment configs |

**When user says**: "Add performance logging" → Use `/sp.performance-logger`
**When user says**: "Prepare for production" → Use `/sp.production-checklist`
**When user says**: "Deploy to Vercel" → Use `/sp.vercel-deployer`

---

#### 7️⃣ Specialized Utility Skills (5 skills)

| Skill | When to Use | Purpose | Output |
|-------|-------------|---------|--------|
| `/sp.api-docs-generator` | Generating API documentation | OpenAPI/Swagger docs, deployment guides | API docs, CHANGELOG.md |
| `/sp.change-management` | Modifying existing features | Impact analysis, safe changes, rollback plan | Change spec, updated files |
| `/sp.skill-creator` | Creating new reusable skills | When new capability needed | New skill in `.claude/skills/` |
| `/sp.github-specialist` | GitHub operations | Issues, PRs, releases, GitHub Actions | GitHub configs, workflows |
| `/sp.conversation-manager` | Managing chat state | Conversation/Message models | Database models, services |

**When user says**: "Document the API" → Use `/sp.api-docs-generator`
**When user says**: "Modify existing feature X" → Use `/sp.change-management`
**When user says**: "Create new skill for Y" → Use `/sp.skill-creator`

---

### 🎯 Feature → Skills Mapping (Common Scenarios)

#### Scenario 1: "Create AI chatbot for task management"
**Required Skills** (Sequential):
1. `/sp.database-schema-expander` → Conversation & Message tables
2. `/sp.mcp-tool-builder` (5x) → add_task, list_tasks, complete_task, update_task, delete_task
3. `/sp.ai-agent-setup` → OpenAI Agents SDK configuration
4. `/sp.chatbot-endpoint` → Stateless chat API
5. `/sp.conversation-manager` → Conversation state management
6. `/sp.edge-case-tester` → Comprehensive testing (auto-trigger)

#### Scenario 2: "Add user authentication"
**Required Skills** (Sequential):
1. `/sp.database-schema-expander` → Users table (if needed)
2. `/sp.jwt-authentication` → JWT creation/verification
3. `/sp.password-security` → bcrypt hashing, auth endpoints
4. `/sp.user-isolation` → Protect all user data
5. `/sp.pydantic-validation` → Auth request/response schemas
6. `/sp.security-engineer` → Security audit

#### Scenario 3: "Performance optimization"
**Required Skills** (Sequential):
1. `/sp.connection-pooling` → Verify pool configuration
2. `/sp.performance-logger` → Add execution time logging
3. `/sp.structured-logging` → JSON logging setup
4. `/sp.database-engineer` → Query optimization, indexes
5. `/sp.ab-testing` → Load testing, performance validation

#### Scenario 4: "Prepare for production deployment"
**Required Skills** (Sequential):
1. `/sp.security-engineer` → OWASP security audit
2. `/sp.performance-logger` → Performance monitoring
3. `/sp.structured-logging` → Production logging
4. `/sp.api-docs-generator` → API documentation
5. `/sp.deployment-automation` → Deployment scripts
6. `/sp.qa-engineer` → Smoke tests
7. `/sp.production-checklist` → Production readiness validation

#### Scenario 5: "Add new feature X from scratch"
**Required Skills** (Sequential):
1. `/sp.new-feature` → Creates spec.md, plan.md, tasks.md
2. `/sp.fullstack-architect` → System design
3. `/sp.backend-developer` → Backend implementation
4. `/sp.frontend-developer` → Frontend implementation
5. `/sp.edge-case-tester` → Edge case testing (auto)
6. `/sp.qa-engineer` → Integration testing

---

### 📊 Skills Usage Patterns

#### Pattern 1: Role-Based Development
When implementing complex features, chain role-based skills:
```text
/sp.fullstack-architect → Overall design
  ↓
/sp.backend-developer → API implementation
  ↓
/sp.frontend-developer → UI implementation
  ↓
/sp.qa-engineer → Testing
```

#### Pattern 2: Foundation First
Always establish foundation before adding features:
```text
/sp.database-schema-expander → Data models
  ↓
/sp.connection-pooling → Database setup
  ↓
/sp.transaction-management → Write operations
  ↓
/sp.backend-developer → Business logic
```

#### Pattern 3: Security & Testing Last
End every feature with security and testing:
```text
[Feature Implementation]
  ↓
/sp.user-isolation → Protect user data
  ↓
/sp.security-engineer → Security audit
  ↓
/sp.edge-case-tester → Edge cases (auto)
  ↓
/sp.qa-engineer → Comprehensive tests
```

### 🎯 Skill Usage Contract

#### Quick Reference: User Request → Skills

**See "Feature → Skills Mapping" section above for 5 complete scenarios.**

**Common Patterns**:
- "Create X" → `/sp.new-feature` (spec→plan→tasks)
- "Implement X" → Role-based skills (`/sp.backend-developer`, `/sp.frontend-developer`)
- "Add authentication" → `/sp.jwt-authentication` + `/sp.password-security` + `/sp.user-isolation`
- "Optimize performance" → `/sp.connection-pooling` + `/sp.performance-logger` + `/sp.database-engineer`
- "Deploy to production" → Production & Deployment skills (5 skills in sequence)
- "Test X" → `/sp.edge-case-tester` + `/sp.qa-engineer`
- "Modify existing feature" → `/sp.change-management`

#### Automatic Skill Triggers (MANDATORY)
- ✅ After `/sp.implement` completes → **MUST** auto-run `/sp.edge-case-tester`
- ✅ After any database write → **SHOULD** use `/sp.transaction-management`
- ✅ After new API endpoint → **SHOULD** use `/sp.pydantic-validation`
- ✅ After any feature completion → **SUGGEST** `/sp.ab-testing` for validation
- ✅ After architecture changes → **SUGGEST** `/sp.adr` (Architecture Decision Record)

### ⚡ Enforcement Mechanism

#### PASS ✅ - Skill-Based Implementation
```text
User: "Add performance logging to all services"
Claude:
  🔧 Skill Plan:
  1. /sp.skill-creator → Create /sp.performance-logger
  2. /sp.performance-logger → Add logging to services

  Waiting for approval... ✋

User: "Approved"
Claude:
  🔧 Using Skill: /sp.skill-creator
  Purpose: Create performance logging skill
  ✅ Skill Complete

  🔧 Using Skill: /sp.performance-logger
  Purpose: Add @log_execution_time decorators
  Files Generated:
    - backend/src/utils/performance.py
    - backend/src/services/conversation_service.py
  ✅ Skill Complete
```

#### FAIL ❌ - Manual Implementation (VIOLATION)
```text
User: "Add performance logging to all services"
Claude: [Creates utils/performance.py manually without using skills]

❌ VIOLATION: Manual implementation without skill usage
✅ CORRECT: Use /sp.skill-creator first, then invoke skill
```

### 📊 Skills Usage Tracking (MANDATORY)

Every feature implementation MUST include:
1. **Skill Execution Plan** - Before starting work
2. **Terminal Skill Output** - During execution (visible to user)
3. **Skills Usage Report** - In PHR and commit message

**PHR Template Requirement:**
```yaml
skills_used:
  - name: /sp.mcp-tool-builder
    tasks: T45-T48
    purpose: Create add_task MCP tool
    files: [src/mcp_tools/add_task.py]
  - name: /sp.edge-case-tester
    tasks: T60-T62
    purpose: Comprehensive edge case testing
    status: 57/57 passed
skills_created:
  - name: /sp.performance-logger
    reason: No existing skill for execution time logging
    location: .claude/skills/sp.performance-logger.md
manual_tasks:
  - task: None (all tasks completed via skills)
violations: None
```

### 🏫 Why Skills Are MANDATORY (Educational Requirement)

**Project teachers/instructors require skill-based approach because:**
1. **Consistency**: Ensures all students follow same patterns
2. **Reusability**: Skills improve and become smarter over time
3. **Constitution Enforcement**: Skills automatically apply project principles
4. **Quality**: Skills include comprehensive testing and validation
5. **Learning**: Students understand feature patterns, not just code
6. **Traceability**: Clear audit trail of what was used when

### 🚫 What Constitutes a Violation

**Violations include:**
- ❌ Implementing features manually when skills exist
- ❌ No terminal output showing skill usage
- ❌ No skill execution plan before starting work
- ❌ Not creating skills for reusable capabilities
- ❌ PHR/commits without skills usage documentation
- ❌ Proceeding without user approval of skill plan

**Consequences of violations:**
- ⚠️ Work must be redone using proper skill-based approach
- ⚠️ Constitution updated to prevent future violations
- ⚠️ Skills created retroactively for violated implementations

### ✅ Skill-Based Development Checklist

Before considering ANY Phase III+ feature complete:
- [ ] Skill execution plan created and approved
- [ ] Terminal output shows which skills were used
- [ ] All applicable skills invoked (or new skills created)
- [ ] Skills usage documented in PHR
- [ ] Skills usage mentioned in commit message
- [ ] No manual implementation where skills exist
- [ ] Constitution principles enforced via skills

**Remember: Skills are NOT optional. They are MANDATORY for all Phase III+ development.**

---

**Version**: 4.0.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2025-12-31 (Phase III Skills Policy Added)