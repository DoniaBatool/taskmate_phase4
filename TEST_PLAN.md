# Comprehensive Test Plan for AI Chat Assistant

## Test Cases to Verify

### ✅ 1. ADD TASK Operations
- [x] "add task" → should ask for title
- [x] "add task: buy milk" → should create task directly
- [x] "create a new task" → should ask for details
- [x] "add task: groceries with high priority" → should create with priority

### ✅ 2. LIST TASKS Operations
- [x] "show my tasks" → should list all tasks
- [x] "list tasks" → should list all tasks
- [x] "view my task list" → should list all tasks
- [x] "show completed tasks" → should filter by status

### ✅ 3. UPDATE TASK Operations
- [x] "update the task" → should ask which task
- [x] "update task #5" → should ask what to update
- [x] "update task #5 to high priority" → should show confirmation
- [x] User says "yes" → should execute update
- [x] User says "no" → should cancel with proper message

### ✅ 4. DELETE TASK Operations
- [x] "delete task" → should ask which task
- [x] "delete task #5" → should ask for confirmation
- [x] User says "yes" → should delete task
- [x] User says "no" → should cancel with "Deletion cancelled"

### ✅ 5. COMPLETE/INCOMPLETE Operations
- [x] "mark task #5 as complete" → should ask confirmation
- [x] "mark task #5 as incomplete" → should ask confirmation
- [x] User says "yes" → should update status
- [x] User says "no" → should cancel properly

### 🎯 Expected Behavior

#### For "add task: buy milk"
- AI agent should parse the request
- Should ask for priority
- Should ask for deadline
- Should create task with all details

#### For "show my tasks"
- Should execute list_tasks tool immediately
- Should display formatted task list with:
  - Task ID
  - Priority (with emojis)
  - Status (✅/⏳)
  - Due date (if set)
  - Title

#### For "update task" (no task specified)
- Should return update_ask intent
- Should list all tasks
- Should ask "Kaunsa task update karna hai?"

#### For "delete task" (no task specified)
- Should return delete_ask intent
- Should list all tasks
- Should ask "Kaunsa task delete karna hai?"

## Error Cases Fixed

### ❌ Previous Errors:
1. "Sorry, I encountered an error" on "add task"
2. "Sorry, I encountered an error" on "show my tasks"
3. "Sorry, I encountered an error" on "delete task"
4. "Update cancelled" shown when user cancels deletion

### ✅ Fixed:
1. add_task: AI agent handles conversation flow
2. list_tasks: Forced execution via intent detector
3. delete_ask: Returns proper intent to ask which task
4. Cancellation messages: Operation-specific (delete → "Deletion cancelled")

## Testing Instructions

1. **Test Add Task:**
   ```
   User: add task
   Expected: "What's the title of the task you'd like to add?"
   
   User: add task: buy milk
   Expected: "Should I add 'buy milk' to your tasks? What priority..."
   ```

2. **Test List Tasks:**
   ```
   User: show my tasks
   Expected: Formatted task list with all details
   
   User: list all tasks
   Expected: Same formatted task list
   ```

3. **Test Update Task:**
   ```
   User: update the task
   Expected: "Kaunsa task update karna hai?" + task list
   
   User: update task #5
   Expected: "Task #5 — what would you like to update?"
   
   User: title to Buy groceries, priority to high
   Expected: Confirmation template with changes
   
   User: yes
   Expected: "✅ I've updated task #5..."
   ```

4. **Test Delete Task:**
   ```
   User: delete task
   Expected: "Kaunsa task delete karna hai?" + task list
   
   User: delete task #5
   Expected: "Kya aap sure hain k task #5 delete karna hai?"
   
   User: no
   Expected: "❌ Deletion cancelled. No task was deleted."
   ```

## Success Criteria

✅ All operations work without "Sorry, I encountered an error"
✅ Proper cancellation messages for all operations
✅ Forced execution for deterministic operations (list, delete confirmed, etc.)
✅ AI agent handles conversational operations (add with details)
✅ Multi-turn conversations work correctly
✅ Date parsing works for "tomorrow", "today", etc.
