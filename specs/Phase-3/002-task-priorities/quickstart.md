# Quickstart Guide: Task Priority System

**Feature**: `002-task-priorities` | **Date**: 2026-01-01
**For**: Developers & End Users

---

## For Developers

### Prerequisites

Before implementing the task priority system, ensure you have:

- ✅ Completed Phase 3 Basic Level (AI chatbot with 5 MCP tools)
- ✅ PostgreSQL database (NeonDB) running and accessible
- ✅ Alembic configured for database migrations
- ✅ Python 3.13+ with FastAPI, SQLModel, OpenAI Agents SDK
- ✅ Next.js 15+ frontend with Tailwind CSS
- ✅ Access to repository: `/home/donia_batool/todo-chatbot-phase3`

### Quick Setup (5 Minutes)

#### 1. Run Database Migration

```bash
# Navigate to backend directory
cd backend

# Create new migration for priority field
alembic revision --autogenerate -m "add_priority_to_tasks"

# Review the generated migration file in alembic/versions/
# Ensure it includes:
# - CREATE TYPE priority_enum AS ENUM ('high', 'medium', 'low')
# - ADD COLUMN priority with default 'medium'
# - CREATE INDEX ix_tasks_user_priority

# Apply the migration
alembic upgrade head

# Verify migration success
psql $DATABASE_URL -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_name='tasks' AND column_name='priority';"
```

**Expected Output**:
```
 column_name |  data_type
-------------+-------------
 priority    | USER-DEFINED
(1 row)
```

#### 2. Update Task Model

**File**: `backend/src/models.py`

```python
from enum import Enum as PyEnum
from sqlalchemy import Column, Enum
from sqlmodel import Field, SQLModel
from datetime import datetime

class PriorityLevel(str, PyEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    title: str = Field(max_length=200, nullable=False)
    description: str | None = Field(default=None)
    completed: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # NEW: Priority field
    priority: str = Field(
        default="medium",
        sa_column=Column(
            Enum("high", "medium", "low", name="priority_enum"),
            nullable=False,
            server_default="medium"
        )
    )
```

#### 3. Update MCP Tools

**File**: `backend/src/mcp_tools/add_task.py`

```python
from pydantic import BaseModel, Field, field_validator

class AddTaskParams(BaseModel):
    user_id: str
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    priority: str = Field(default="medium", pattern="^(high|medium|low)$")

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: str) -> str:
        if v not in ["high", "medium", "low"]:
            raise ValueError(f"Invalid priority: {v}. Must be 'high', 'medium', or 'low'.")
        return v

def add_task(db: Session, params: AddTaskParams) -> dict:
    task = Task(
        user_id=int(params.user_id),
        title=params.title,
        description=params.description,
        priority=params.priority  # NEW: Include priority
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "success": True,
        "task": task,
        "message": f"Task created successfully with {params.priority} priority"
    }
```

**Repeat for**:
- `backend/src/mcp_tools/update_task.py` (add priority parameter)
- `backend/src/mcp_tools/list_tasks.py` (add priority filter)

#### 4. Update AI Agent System Prompt

**File**: `backend/src/ai_agent/runner.py`

```python
SYSTEM_PROMPT = """
You are a task management assistant. Help users manage their tasks through natural language.

When users mention priorities, map synonyms to standard values:
- "high", "urgent", "critical", "important" → priority: "high"
- "medium", "normal" → priority: "medium"
- "low", "minor", "trivial", "someday" → priority: "low"
- No mention → default to "medium"

Examples:
- "add urgent task to fix bug" → Call add_task with priority="high"
- "create task to buy milk" → Call add_task with priority="medium"
- "add minor task to organize files" → Call add_task with priority="low"
- "show me all high priority tasks" → Call list_tasks with priority="high"
- "change task 5 to low priority" → Call update_task with priority="low"
"""
```

#### 5. Add Frontend Priority Badge Component

**File**: `frontend/components/PriorityBadge.tsx`

```tsx
export function PriorityBadge({ priority }: { priority: 'high' | 'medium' | 'low' }) {
  const className = `priority-badge-${priority} px-2 py-0.5 rounded-full text-xs font-medium`;
  const label = priority.charAt(0).toUpperCase() + priority.slice(1);

  return (
    <span className={className} aria-label={`Priority: ${label}`}>
      {label}
    </span>
  );
}
```

**File**: `frontend/app/globals.css`

```css
/* Priority badges - Dark mode (default) */
.priority-badge-high {
  background-color: #dc2626; /* red-600 */
  color: #ffffff;
}

.priority-badge-medium {
  background-color: #f59e0b; /* amber-500 */
  color: #000000;
}

.priority-badge-low {
  background-color: #16a34a; /* green-600 */
  color: #ffffff;
}

/* Priority badges - Light mode */
html.light .priority-badge-high {
  background-color: #ef4444; /* red-500 */
  color: #ffffff;
}

html.light .priority-badge-medium {
  background-color: #fbbf24; /* amber-400 */
  color: #000000;
}

html.light .priority-badge-low {
  background-color: #15803d; /* green-700 */
  color: #ffffff;
}
```

**File**: `frontend/components/TaskItem.tsx` (modify)

```tsx
import { PriorityBadge } from './PriorityBadge';

export function TaskItem({ task }: { task: Task }) {
  return (
    <div className="task-item">
      <h3>{task.title}</h3>
      <PriorityBadge priority={task.priority} />
      {/* ... rest of task display ... */}
    </div>
  );
}
```

#### 6. Update TypeScript Types

**File**: `frontend/lib/types.ts`

```typescript
export interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string | null;
  completed: boolean;
  priority: 'high' | 'medium' | 'low';  // NEW
  created_at: string;
  updated_at: string;
}
```

#### 7. Start Services

```bash
# Terminal 1: Start backend
cd backend
uvicorn src.main:app --reload --port 8000

# Terminal 2: Start frontend
cd frontend
npm run dev
```

#### 8. Test the Feature

```bash
# Test chatbot endpoint
curl -X POST http://localhost:8000/api/user_12345/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "add high priority task to buy groceries"}'

# Expected response includes task with priority="high"
```

### Testing Checklist

Run these tests to verify implementation:

**Backend Tests** (`backend/tests/`):
```bash
# Run priority MCP tool tests
pytest tests/test_mcp_priority.py -v

# Run NLP extraction tests
pytest tests/test_priority_nlp.py -v

# Run all tests
pytest tests/ -v
```

**Frontend Tests**:
```bash
# Run component tests
cd frontend
npm test -- PriorityBadge.test.tsx
```

**Manual E2E Test**:
1. ✅ Create high priority task: "add urgent task to submit report"
2. ✅ Verify red badge appears in task list
3. ✅ Create low priority task: "add task to organize garage someday"
4. ✅ Verify green badge appears
5. ✅ Update priority: "change task 1 to low priority"
6. ✅ Verify badge changes from red to green
7. ✅ Filter tasks: "show me all high priority tasks"
8. ✅ Verify only high priority tasks displayed
9. ✅ Test light/dark mode toggle
10. ✅ Verify WCAG contrast ratios with browser DevTools

### Troubleshooting

**Issue**: Migration fails with "type priority_enum already exists"
```bash
# Solution: Drop existing type and re-run migration
psql $DATABASE_URL -c "DROP TYPE IF EXISTS priority_enum CASCADE;"
alembic upgrade head
```

**Issue**: Frontend shows TypeScript errors for priority field
```bash
# Solution: Regenerate types from backend schema
cd frontend
npm run generate-types  # If using codegen
# Or manually update lib/types.ts
```

**Issue**: Badge colors not appearing
```bash
# Solution: Ensure globals.css is imported in layout.tsx
# frontend/app/layout.tsx
import './globals.css';
```

**Issue**: AI agent not extracting priority
```bash
# Solution: Verify system prompt in backend/src/ai_agent/runner.py
# Check OpenAI Agents SDK configuration includes tools with priority parameter
```

### Development Workflow

1. **Create Feature Branch** (if not on main):
   ```bash
   git checkout -b 002-task-priorities
   ```

2. **Make Changes**: Follow steps 1-6 above

3. **Run Tests**: Ensure all tests pass

4. **Commit Changes**:
   ```bash
   git add .
   git commit -m "feat: add task priority system with 3 levels (high/medium/low)"
   ```

5. **Create Pull Request** (if using feature branches):
   ```bash
   gh pr create --title "Task Priority System" --body "Implements 3-level priority system with WCAG-compliant badges"
   ```

### Performance Verification

Run these queries to verify index usage:

```sql
-- Verify composite index exists
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'tasks' AND indexname = 'ix_tasks_user_priority';

-- Test query plan (should use index scan)
EXPLAIN ANALYZE
SELECT * FROM tasks
WHERE user_id = 12345 AND priority = 'high';
```

**Expected**: Query plan shows "Index Scan using ix_tasks_user_priority"

### Accessibility Testing

Use these tools to verify WCAG compliance:

1. **WebAIM Contrast Checker**: https://webaim.org/resources/contrastchecker/
   - High (dark): #dc2626 on #0f172a → Should show ≥4.5:1
   - Medium (dark): #f59e0b on #0f172a → Should show ≥4.5:1
   - Low (dark): #16a34a on #0f172a → Should show ≥4.5:1

2. **Chrome DevTools**:
   - Inspect badge element
   - Check color picker for contrast ratio
   - Should show green checkmark for AA compliance

3. **Lighthouse**:
   ```bash
   cd frontend
   npm run build
   npx lighthouse http://localhost:3000/tasks --view
   ```
   - Accessibility score should be ≥90

---

## For End Users

### What's New: Task Priorities

You can now assign priorities to your tasks to help organize what's most important!

### How to Use Priorities

#### Creating Tasks with Priority

Just tell the chatbot what priority you want:

**Examples**:
- "Add high priority task to submit report by Friday"
- "Create urgent task to fix production bug"
- "Add task to buy groceries" (defaults to medium priority)
- "Remind me to organize garage someday" (creates low priority task)

**Keywords that mean HIGH priority**:
- "high priority"
- "urgent"
- "critical"
- "important"

**Keywords that mean LOW priority**:
- "low priority"
- "minor"
- "trivial"
- "someday"

**No keywords?** Your task gets MEDIUM priority automatically.

#### Changing Task Priority

Tell the chatbot to update the priority:

**Examples**:
- "Change task 5 to high priority"
- "Make task 3 urgent"
- "Set task 10 as low priority"
- "Update task 2 to normal priority"

#### Viewing Tasks by Priority

Filter your tasks to focus on what matters:

**Examples**:
- "Show me all high priority tasks"
- "List my urgent tasks"
- "What are my low priority tasks?"
- "Show incomplete high priority tasks"

### Understanding Priority Badges

Tasks now display colored badges:

- 🔴 **Red Badge** = HIGH PRIORITY (urgent, important)
- 🟡 **Yellow Badge** = MEDIUM PRIORITY (normal, default)
- 🟢 **Green Badge** = LOW PRIORITY (minor, can wait)

The badges work in both light and dark modes!

### Common Workflows

#### Planning Your Day
```
You: "Show me all high priority tasks"
Bot: [Lists urgent tasks with red badges]

You: "Show incomplete high priority tasks"
Bot: [Lists only unfinished urgent tasks]
```

#### Creating a Shopping List
```
You: "Add low priority task to buy milk"
Bot: "Task created with low priority" [Green badge appears]

You: "Actually, make that task high priority"
Bot: "Task updated to high priority" [Badge changes to red]
```

#### Organizing a Project
```
You: "Add high priority task to submit final report"
You: "Add medium priority task to review team feedback"
You: "Add low priority task to organize project files"
Bot: [Creates 3 tasks with red, yellow, and green badges]
```

### Tips for Using Priorities

✅ **DO**:
- Use high priority for urgent deadlines
- Use medium priority for regular tasks
- Use low priority for "nice to have" tasks
- Update priorities as deadlines change

❌ **DON'T**:
- Make everything high priority (defeats the purpose!)
- Forget to update priorities when circumstances change
- Ignore low priority tasks forever (they can still be valuable)

### Accessibility Features

- All priority badges have high contrast for visibility
- Screen readers announce priority level
- Color is not the only indicator (text labels included)
- Works with keyboard navigation

### Quick Reference

| What You Say | Priority Level | Badge Color |
|-------------|----------------|-------------|
| "urgent task..." | High | Red 🔴 |
| "important task..." | High | Red 🔴 |
| "critical task..." | High | Red 🔴 |
| "task to..." (no keyword) | Medium | Yellow 🟡 |
| "normal task..." | Medium | Yellow 🟡 |
| "minor task..." | Low | Green 🟢 |
| "task someday..." | Low | Green 🟢 |

### Getting Help

If you need assistance:
- Ask the chatbot: "How do I set task priorities?"
- Try: "What priority levels are available?"
- Contact support if badges aren't displaying correctly

---

## Additional Resources

### Developer Documentation
- [spec.md](./spec.md) - Complete feature specification
- [plan.md](./plan.md) - Implementation plan
- [data-model.md](./data-model.md) - Database schema
- [research.md](./research.md) - Technical decisions
- [contracts/](./contracts/) - MCP tool API contracts

### External Links
- [WCAG 2.1 AA Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [OpenAI Agents SDK Documentation](https://platform.openai.com/docs)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Tailwind CSS Customization](https://tailwindcss.com/docs/customizing-colors)

### Support

For technical issues:
- Check troubleshooting section above
- Review test failures with `pytest -v`
- Verify database schema with `psql $DATABASE_URL`
- Inspect browser console for frontend errors

For feature requests:
- Review `spec.md` to see what's in scope
- Check "Out of Scope" section for planned future features
- Document requests for Phase 3 Advanced Level features

---

**Last Updated**: 2026-01-01
**Version**: 1.0.0
**Status**: Ready for Implementation
