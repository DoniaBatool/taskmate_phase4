# Tasks: Task Priority System

**Feature**: `002-task-priorities` | **Date**: 2026-01-01
**Input**: Design documents from `/specs/Phase-3/002-task-priorities/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/, research.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

This project uses web app structure with:
- **Backend**: `backend/src/`, `backend/tests/`, `backend/alembic/`
- **Frontend**: `frontend/app/`, `frontend/components/`, `frontend/lib/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and database schema preparation

- [x] T001 Create Alembic migration for priority field in backend/alembic/versions/
- [x] T002 Apply database migration to add priority column with ENUM type and index
- [x] T003 Verify migration success and existing tasks have default 'medium' priority

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Update Task model with priority field in backend/src/models.py
- [x] T005 [P] Add PriorityLevel enum to backend/src/models.py
- [x] T006 [P] Update Task type definition with priority field in frontend/lib/types.ts
- [x] T007 Update AI agent system prompt with priority synonym mapping in backend/src/ai_agent/agent.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Set Priority When Creating Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to assign priority levels (high, medium, low) when creating tasks through the AI chatbot using natural language commands.

**Independent Test**: Create tasks via chatbot with "add high priority task to buy groceries", "add task to call mom" (defaults to medium), and "low priority task: organize photos". Verify priority is stored in database and displayed with correct badge colors.

### Implementation for User Story 1

- [x] T008 [P] [US1] Create PriorityBadge component in frontend/components/PriorityBadge.tsx
- [x] T009 [P] [US1] Add priority badge styles to frontend/app/globals.css (light and dark modes)
- [x] T010 [US1] Update add_task MCP tool with priority parameter in backend/src/mcp_tools/add_task.py
- [x] T011 [US1] Add priority validation to AddTaskParams Pydantic model in backend/src/mcp_tools/add_task.py
- [x] T012 [US1] Update TaskItem component to display PriorityBadge in frontend/components/TaskItem.tsx
- [x] T013 [US1] Verify MCP tool returns task with priority field in response

**Checkpoint**: At this point, User Story 1 should be fully functional - users can create tasks with priority and see color-coded badges

---

## Phase 4: User Story 4 - Visual Priority Indicators (Priority: P1)

**Goal**: Tasks display color-coded priority badges in both light and dark modes for easy visual identification with WCAG 2.1 AA compliance.

**Independent Test**: View tasks with different priorities in both light and dark modes. Verify badges display with correct colors (high=red, medium=yellow, low=green) and meet 4.5:1 contrast ratio in both themes.

**Note**: Most implementation completed in US1 (PriorityBadge component + styles). This phase focuses on accessibility validation and theme integration.

### Implementation for User Story 4

- [x] T014 [P] [US4] Verify WCAG contrast ratios for all badge colors in light mode using WebAIM checker
- [x] T015 [P] [US4] Verify WCAG contrast ratios for all badge colors in dark mode using WebAIM checker
- [x] T016 [US4] Add aria-label to PriorityBadge for screen reader accessibility in frontend/components/PriorityBadge.tsx
- [x] T017 [US4] Update tasks list page to display priority badges in frontend/app/tasks/page.tsx
- [x] T018 [US4] Test badge visibility with color blindness simulators

**Checkpoint**: All priority badges are accessible and visually distinct in both themes

---

## Phase 5: User Story 2 - Update Task Priority (Priority: P2)

**Goal**: Allow users to change the priority level of existing tasks through the AI chatbot using natural language.

**Independent Test**: Create a task with medium priority, then use chatbot to say "change task 1 to high priority" and "make task 1 low priority". Verify priority updates are reflected in database and badge changes color accordingly.

### Implementation for User Story 2

- [x] T019 [P] [US2] Update update_task MCP tool with priority parameter in backend/src/mcp_tools/update_task.py
- [x] T020 [P] [US2] Add priority validation to UpdateTaskParams Pydantic model in backend/src/mcp_tools/update_task.py
- [x] T021 [US2] Implement priority change detection in update_task response message in backend/src/mcp_tools/update_task.py
- [x] T022 [US2] Update updated_at timestamp when priority changes in backend/src/mcp_tools/update_task.py
- [x] T023 [US2] Test idempotent priority updates (updating to same value)

**Checkpoint**: Users can update task priorities via chatbot and changes are immediately visible

---

## Phase 6: User Story 3 - Filter Tasks by Priority (Priority: P3)

**Goal**: Enable users to view tasks filtered by priority level through the AI chatbot.

**Independent Test**: Create tasks with mixed priorities (high, medium, low), then use chatbot to say "show me high priority tasks" and "list low priority items". Verify only tasks matching the filter are returned and displayed.

### Implementation for User Story 3

- [x] T024 [P] [US3] Update list_tasks MCP tool with priority filter parameter in backend/src/mcp_tools/list_tasks.py
- [x] T025 [P] [US3] Add priority validation to ListTasksParams Pydantic model in backend/src/mcp_tools/list_tasks.py
- [x] T026 [US3] Implement SQL query filtering by priority using composite index in backend/src/mcp_tools/list_tasks.py
- [x] T027 [US3] Update response message to indicate filter applied (e.g., "Found 2 high priority tasks")
- [x] T028 [US3] Handle empty results with friendly message ("You have no high priority tasks")
- [x] T029 [US3] Test combined filters (priority + completion status)

**Checkpoint**: All user stories (1-4) are now complete and independently functional

---

## Phase 7: Integration & E2E Testing

**Purpose**: Verify all user stories work together correctly

- [x] T030 [P] Test full workflow: Create → Update → Filter → Display with priority badges
- [x] T031 [P] Test AI agent synonym recognition (urgent→high, minor→low, normal→medium)
- [x] T032 [P] Test edge cases from spec.md (invalid priority, ambiguous commands, non-existent tasks)
- [x] T033 Verify backward compatibility (existing tasks have medium priority)
- [x] T034 Verify user isolation (User A cannot see/modify User B's task priorities)
- [x] T035 [P] Test performance: priority filtering adds <50ms to queries
- [x] T036 [P] Run Lighthouse accessibility audit on tasks page (score ≥90)

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T037 [P] Add comprehensive docstrings to all modified MCP tools in backend/src/mcp_tools/
- [x] T038 [P] Update API documentation with priority parameter details
- [x] T039 Code cleanup: Remove any debug logging from priority implementation
- [x] T040 [P] Performance optimization: Verify composite index (user_id, priority) is used in queries
- [x] T041 [P] Add unit tests for PriorityLevel enum validation in backend/tests/
- [x] T042 [P] Add React component tests for PriorityBadge in frontend/components/
- [x] T043 Security review: Verify priority validation prevents SQL injection
- [x] T044 Run quickstart.md validation for developer setup steps
- [x] T045 [P] Update project README with priority system documentation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1 (Create with Priority) - Can start after Foundational
  - US4 (Visual Indicators) - Depends on US1 (requires PriorityBadge component)
  - US2 (Update Priority) - Can start after Foundational (independent of US1)
  - US3 (Filter by Priority) - Can start after Foundational (independent of US1)
- **Integration Testing (Phase 7)**: Depends on US1, US2, US3, US4 completion
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P1)**: Depends on User Story 1 (requires PriorityBadge component from US1)
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

**User Story 1**:
- T008 (PriorityBadge component) and T009 (CSS styles) can run in parallel [P]
- T010 (MCP tool) must complete before T011 (validation)
- T012 (TaskItem) depends on T008 (PriorityBadge component exists)

**User Story 4**:
- T014 and T015 (WCAG verification) can run in parallel [P]
- T016 (aria-label) can run in parallel with verification tasks
- T017 (tasks page) depends on T016 (PriorityBadge is accessible)

**User Story 2**:
- T019 (MCP tool) and T020 (validation) can run in parallel [P]
- T021 (change detection) depends on T019

**User Story 3**:
- T024 (MCP tool) and T025 (validation) can run in parallel [P]
- T026 (SQL filtering) depends on T024

### Parallel Opportunities

- **Phase 1**: T001-T003 must run sequentially (migration order)
- **Phase 2**: T005, T006 can run in parallel [P] after T004
- **Phase 3 (US1)**: T008, T009 can run in parallel [P]
- **Phase 4 (US4)**: T014, T015, T016 can run in parallel [P]
- **Phase 5 (US2)**: T019, T020 can run in parallel [P]
- **Phase 6 (US3)**: T024, T025 can run in parallel [P]
- **Phase 7**: T030, T031, T032, T035, T036 can run in parallel [P]
- **Phase 8**: T037, T038, T040, T041, T042, T045 can run in parallel [P]

### Story-Level Parallelization

After Foundational phase (Phase 2) completes:
- **US1 + US2 + US3** can be developed in parallel by different developers
- **US4** MUST wait for US1 to complete (depends on PriorityBadge component)

**Optimal Team Strategy**:
1. Complete Phase 1 + Phase 2 together (sequential, blocking)
2. Split team:
   - Developer A: US1 (Create) → US4 (Visual)
   - Developer B: US2 (Update)
   - Developer C: US3 (Filter)
3. Integrate in Phase 7

---

## Parallel Example: User Story 1

```bash
# Launch parallel tasks for User Story 1:

# Parallel Group 1 (frontend components):
Task T008: "Create PriorityBadge component in frontend/components/PriorityBadge.tsx"
Task T009: "Add priority badge styles to frontend/app/globals.css"

# Sequential (backend - requires order):
Task T010: "Update add_task MCP tool with priority parameter"
Task T011: "Add priority validation to AddTaskParams" (depends on T010)

# Final integration:
Task T012: "Update TaskItem to display PriorityBadge" (depends on T008)
Task T013: "Verify MCP tool response includes priority"
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 4 Only)

This delivers the minimum viable product for the priority system:

1. **Complete Phase 1**: Setup (T001-T003) - Database ready
2. **Complete Phase 2**: Foundational (T004-T007) - Models and AI agent ready
3. **Complete Phase 3**: User Story 1 (T008-T013) - Users can create tasks with priority
4. **Complete Phase 4**: User Story 4 (T014-T018) - Badges are accessible and visible
5. **STOP and VALIDATE**: Test creating tasks with different priorities and viewing badges
6. **Deploy/Demo**: MVP is ready for user feedback

**MVP Scope**: 18 tasks (T001-T018)
**Delivers**: Core value proposition - users can set priorities when creating tasks and see visual indicators

### Incremental Delivery

Each user story adds value independently:

1. **MVP (US1 + US4)** → Deploy: Users can create tasks with priority and see badges
2. **+ US2 (Update)** → Deploy: Users can now update task priorities
3. **+ US3 (Filter)** → Deploy: Users can filter tasks by priority
4. **+ Phase 7 (Integration)** → Deploy: Full E2E testing complete
5. **+ Phase 8 (Polish)** → Deploy: Production-ready with docs and optimizations

### Parallel Team Strategy

With 3 developers after Foundational phase:

**Week 1**:
- Team: Complete Phase 1 + Phase 2 together (T001-T007)

**Week 2** (Parallel work):
- Developer A: User Story 1 + User Story 4 (T008-T018) - 11 tasks
- Developer B: User Story 2 (T019-T023) - 5 tasks
- Developer C: User Story 3 (T024-T029) - 6 tasks

**Week 3**:
- Team: Integration testing (Phase 7) + Polish (Phase 8)
- Deploy complete feature

**Total**: 45 tasks, 3 weeks with 3 developers (or 5-6 weeks solo)

---

## Performance Checkpoints

### Database Query Performance

- **T002**: After migration, verify index exists: `ix_tasks_user_priority`
- **T026**: Verify `EXPLAIN ANALYZE` shows index scan (not sequential scan)
- **T035**: Benchmark priority filtering <50ms for 10,000 tasks

### Frontend Performance

- **T009**: Verify CSS classes are cached (not inline styles)
- **T017**: Verify badge rendering has no measurable impact on task list render time
- **T036**: Lighthouse performance score remains ≥90

### AI Agent Performance

- **T007**: Test priority extraction latency <100ms per message
- **T031**: Verify synonym recognition accuracy ≥95%

---

## Testing Checklist

### Database Layer
- ✅ Migration creates priority column with ENUM type
- ✅ Default value 'medium' applied to existing tasks
- ✅ Composite index (user_id, priority) exists
- ✅ ENUM constraint rejects invalid values

### Backend MCP Tools
- ✅ add_task accepts priority parameter (defaults to medium)
- ✅ update_task updates priority and refreshes updated_at
- ✅ list_tasks filters by priority with 100% accuracy
- ✅ Invalid priority values return error (not database exception)

### AI Agent NLP
- ✅ Synonym recognition: urgent→high, important→high, minor→low, normal→medium
- ✅ Default to medium when no priority mentioned
- ✅ Extraction accuracy ≥95% on test cases from spec.md

### Frontend Components
- ✅ PriorityBadge displays correct color for each priority level
- ✅ Badges work in both light and dark modes
- ✅ WCAG 2.1 AA contrast ratios (≥4.5:1) verified
- ✅ aria-label present for screen readers

### E2E Workflows
- ✅ Create high priority task → Badge is red
- ✅ Create task without priority → Badge is yellow (medium)
- ✅ Update task from medium to high → Badge changes to red
- ✅ Filter by high priority → Only high priority tasks shown
- ✅ User isolation: User A cannot modify User B's task priorities

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MVP = US1 + US4 (18 tasks) - delivers core value
- Full feature = All 45 tasks - production-ready
- Estimated effort: 3-4 hours solo (per research.md)

---

## Success Criteria Mapping

| Success Criterion | Related Tasks | Verification |
|------------------|---------------|--------------|
| SC-001: Task creation < 5 seconds | T010, T013 | E2E timing test |
| SC-002: Visual distinguishability | T008, T009, T014-T015 | Manual inspection |
| SC-003: WCAG 2.1 AA compliance | T014, T015, T016, T036 | WebAIM + Lighthouse |
| SC-004: 100% filter accuracy | T026, T029 | SQL query validation |
| SC-005: 95% NLP accuracy | T007, T031 | Synonym test suite |
| SC-006: Update < 2 seconds | T019, T023 | E2E timing test |
| SC-007: Color-only identification | T009, T018 | Color blindness simulator |

---

**Last Updated**: 2026-01-01
**Status**: Ready for Implementation
**Total Tasks**: 45 (18 for MVP)
