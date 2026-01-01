# Implementation Plan: Task Priority System

**Feature**: `002-task-priorities` | **Date**: 2026-01-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/Phase-3/002-task-priorities/spec.md`

## Summary

Add a three-level priority system (high, medium, low) to the existing task management chatbot. Users will be able to set priorities via natural language through the AI chatbot ("add high priority task"), update priorities, and filter tasks by priority. The system will display color-coded badges (red/yellow/green) in both light and dark modes with WCAG 2.1 AA accessibility compliance.

**Technical Approach**: Extend existing Task model with priority field, update MCP tools (add_task, update_task, list_tasks) to support priority operations, enhance AI agent NLP to extract priority keywords, and implement theme-aware priority badges in frontend.

## Technical Context

**Language/Version**:
- Backend: Python 3.13+
- Frontend: TypeScript (Next.js 15+)

**Primary Dependencies**:
- Backend: FastAPI, SQLModel, OpenAI Agents SDK, Official MCP SDK
- Frontend: Next.js 15+, React 18+, Tailwind CSS

**Storage**:
- NeonDB (Serverless PostgreSQL)
- New column: `tasks.priority` (enum: 'high' | 'medium' | 'low', default: 'medium')

**Testing**:
- Backend: pytest for MCP tool priority operations
- Frontend: React Testing Library for badge components
- E2E: Chatbot NLP testing for priority extraction

**Target Platform**:
- Backend: Linux server (FastAPI on Uvicorn)
- Frontend: Web browser (Next.js deployed on Vercel)

**Project Type**: Web application (monorepo with frontend + backend)

**Performance Goals**:
- Priority filtering adds < 50ms to task list queries
- Badge rendering has no measurable impact on UI performance
- NLP priority extraction < 100ms per chat message

**Constraints**:
- WCAG 2.1 AA compliance (4.5:1 contrast ratio) for all badges
- User isolation maintained (priority updates respect task ownership)
- Backward compatibility (existing tasks default to 'medium' priority)

**Scale/Scope**:
- Supports 10,000+ users
- 3 priority levels (not extensible in this phase)
- 5 MCP tools updated (add_task, update_task, list_tasks + 2 existing)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Spec-Driven Development
- ✅ Complete specification exists (`specs/Phase-3/002-task-priorities/spec.md`)
- ✅ User stories and acceptance criteria defined
- ✅ Specification approved and validated (zero NEEDS CLARIFICATION markers)

### ✅ II. Full-Stack Code Quality Standards
- ✅ Backend: Will follow PEP 8, type hints, docstrings, <50 line functions
- ✅ Frontend: TypeScript strict mode, ESLint/Prettier, reusable components

### ✅ III. Persistent Multi-User Storage
- ✅ Priority data persisted in NeonDB PostgreSQL
- ✅ SQLModel ORM for database operations
- ✅ User isolation maintained (priority scoped to user_id)
- ✅ Alembic migration for schema change

### ✅ IV. RESTful API Architecture
- ✅ No new API endpoints (extends existing MCP tools)
- ✅ Priority added to existing `/api/{user_id}/chat` chatbot endpoint
- ✅ MCP tools updated in-place (add_task, update_task, list_tasks)
- ✅ Pydantic validation for priority enum values

### ✅ V. Authentication & Security
- ✅ No authentication changes required
- ✅ JWT validation continues on chat endpoint
- ✅ User ID verification enforced on priority updates
- ✅ Task ownership enforcement continues

### ✅ VI. Core Feature Completeness
- ✅ Extends existing features (Add, Update, View)
- ✅ No impact on Delete or Mark Complete features
- ✅ End-to-end: Frontend UI → AI Chat → MCP Tools → Database

**GATE STATUS**: ✅ **PASSED** - All constitution requirements met

## Project Structure

### Documentation (this feature)

```text
specs/Phase-3/002-task-priorities/
├── spec.md              # Feature specification (COMPLETED)
├── plan.md              # This file (IN PROGRESS)
├── research.md          # Phase 0 output (NEXT)
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (MCP tool schemas)
│   ├── add_task.yaml
│   ├── update_task.yaml
│   └── list_tasks.yaml
├── checklists/
│   └── requirements.md  # Quality checklist (COMPLETED)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models.py                    # [MODIFY] Add priority field to Task model
│   ├── routes/
│   │   └── chat.py                  # [MODIFY] Update chat endpoint for priority
│   ├── mcp_tools/
│   │   ├── add_task.py             # [MODIFY] Add priority parameter
│   │   ├── update_task.py          # [MODIFY] Add priority parameter
│   │   └── list_tasks.py           # [MODIFY] Add priority filtering
│   ├── ai_agent/
│   │   └── runner.py               # [MODIFY] Enhance NLP for priority extraction
│   └── db.py                       # [NO CHANGE]
├── alembic/
│   └── versions/
│       └── [NEW]_add_priority_to_tasks.py  # [CREATE] Migration script
└── tests/
    ├── test_mcp_priority.py        # [CREATE] Priority MCP tool tests
    └── test_priority_nlp.py        # [CREATE] NLP extraction tests

frontend/
├── app/
│   ├── tasks/page.tsx              # [MODIFY] Add priority badges
│   └── chat/page.tsx               # [NO CHANGE] Handles via existing chat
├── components/
│   ├── TaskItem.tsx                # [MODIFY] Add PriorityBadge component
│   ├── PriorityBadge.tsx           # [CREATE] New priority badge component
│   └── TaskForm.tsx                # [MODIFY] Optional priority selection in form
├── lib/
│   └── types.ts                    # [MODIFY] Add priority to Task type
└── app/globals.css                  # [MODIFY] Add priority badge styles
```

**Structure Decision**: Web application structure (Option 2) selected. Existing monorepo with frontend/ and backend/ directories. This feature extends existing models and components rather than creating new modules. Migration-based approach for database schema changes.

## Complexity Tracking

> No constitution violations - this section is not applicable.

This feature adheres to all constitution principles:
- No new projects or repositories
- No new architectural patterns
- Extends existing MCP tool architecture
- Maintains existing security and authentication
- Follows established database migration patterns

## Phase 0: Research

**Objective**: Resolve all technical unknowns identified in Technical Context

### Research Tasks

All technical context items are already known from existing Phase 3 implementation:

1. ✅ **Database Schema Evolution**: Alembic migrations already in use
2. ✅ **MCP Tool Extension Pattern**: Existing 5 MCP tools provide reference implementation
3. ✅ **NLP Priority Extraction**: OpenAI Agents SDK supports function calling with parameter extraction
4. ✅ **Frontend Badge Styling**: Tailwind CSS + globals.css pattern established for light/dark themes
5. ✅ **WCAG Compliance**: Color contrast checking tools available (WebAIM, Chrome DevTools)

**Status**: No unknowns remain - proceed directly to Phase 1

### Key Decisions

| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| **Enum type for priority** | Database-level validation, type safety, prevents invalid values | String field with application validation (rejected: less robust), Integer codes (rejected: less readable) |
| **Default to 'medium'** | Balanced starting point, encourages explicit prioritization, backward compatible | Default to 'low' (rejected: discourages important tasks), No default (rejected: forces user input) |
| **Color scheme: Red/Yellow/Green** | Universal urgency signaling (traffic light metaphor), accessible to most users | Blue/Purple/Pink (rejected: no urgency association), Single color with opacity (rejected: less accessible) |
| **NLP synonym recognition** | Improves user experience, handles natural variations | Strict keyword matching (rejected: too rigid), AI interpretation (rejected: unpredictable) |
| **Badge-only visual** | Minimal UI clutter, follows existing design system | Icons + badges (rejected: redundant), Priority dropdown (rejected: too complex for list view) |

## Phase 1: Design & Contracts

### Data Model (see `data-model.md`)

**Entity**: Task (extended)

**New Field**:
```python
priority: str = Field(default="medium", sa_column=Column(Enum("high", "medium", "low", name="priority_enum")))
```

**Validation Rules**:
- Must be one of: "high", "medium", "low"
- Defaults to "medium" for backward compatibility
- Non-nullable (always has a value)

**Migration Strategy**:
- Add column with default value
- Existing rows automatically receive 'medium' priority
- Create enum type in PostgreSQL
- Add index on (user_id, priority) for filtering performance

### API Contracts (see `contracts/`)

**Modified MCP Tools**:

1. **add_task**
   - Add optional `priority` parameter (default: "medium")
   - Returns: task object including priority field
   - Contract: `contracts/add_task.yaml`

2. **update_task**
   - Add optional `priority` parameter
   - Returns: updated task object with new priority
   - Contract: `contracts/update_task.yaml`

3. **list_tasks**
   - Add optional `priority` filter parameter
   - Returns: filtered task list
   - Contract: `contracts/list_tasks.yaml`

### Quickstart (see `quickstart.md`)

**For Developers**:
1. Run migration: `alembic upgrade head`
2. Test MCP tools with priority: `pytest tests/test_mcp_priority.py`
3. Start backend: `uvicorn main:app --reload`
4. Test chatbot: "add high priority task to test"
5. Verify badge display in frontend

**For Users**:
1. Create task: "add high priority task to buy milk"
2. Update task: "change task 1 to low priority"
3. Filter tasks: "show me all high priority tasks"
4. Visual check: Verify red/yellow/green badges in task list

## Phase 2: Implementation Planning

**Not executed by `/sp.plan` - use `/sp.tasks` command next**

This phase will break down the implementation into atomic, testable tasks with specific file paths and acceptance criteria.

## Next Steps

1. ✅ **Phase 0 Complete**: No research needed (all technical decisions known)
2. → **Phase 1 In Progress**: Create `data-model.md`, `contracts/`, `quickstart.md`
3. → **Run `/sp.tasks`**: Generate implementation task breakdown
4. → **Execute Tasks**: Implement via generated task list

## Success Criteria Mapping

| Success Criterion | Implementation Plan |
|-------------------|-------------------|
| SC-001: Task creation < 5 seconds | NLP extraction + MCP tool update < 100ms, UI response immediate |
| SC-002: Visual distinguishability | 3 distinct colors (red/yellow/green) with badge labels |
| SC-003: WCAG 2.1 AA compliance | Test with WebAIM contrast checker, enforce 4.5:1 minimum |
| SC-004: 100% filter accuracy | SQL WHERE clause on priority enum (guaranteed correctness) |
| SC-005: 95% NLP accuracy | Test suite with 20+ priority phrases, synonym mapping |
| SC-006: Update < 2 seconds | MCP tool update + UI re-render < 500ms total |
| SC-007: Color-only identification | Distinct hues (0°/60°/120° HSL), saturation >50% |

## Open Questions

*None - all technical decisions finalized in this plan*

## Architectural Decision Record (ADR)

**Note**: If significant architectural decisions were made during planning, document them with `/sp.adr [decision-title]`.

For this feature, key decisions documented above are:
1. Enum type for priority field (database-level validation)
2. Default to 'medium' priority (backward compatibility)
3. Red/Yellow/Green color scheme (universal urgency signaling)

These do not require separate ADRs as they are:
- Standard patterns (enum for constrained values)
- Non-controversial (common UX conventions)
- Reversible (can change colors/defaults without migration)
