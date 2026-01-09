# Testing Guide: Update/Delete Task Fix

## Quick Test (5 minutes)

### 1. Run Test Script
```bash
cd /home/donia_batool/todo-chatbot-phase3/backend
source venv/bin/activate
python scripts/test_update_delete.py
```

**Expected:** All 3 tests pass with ✓

---

### 2. Test via Chatbot UI

#### Setup
```bash
# Terminal 1: Start backend
cd backend
source venv/bin/activate
uvicorn src.main:app --reload

# Terminal 2: Watch logs
cd backend
tail -f logs/backend.log
```

#### Test Scenario 1: Update Task
1. Open chatbot at `http://localhost:3000`
2. Say: **"Add task: Buy groceries"**
3. Note task ID (e.g., 5)
4. Say: **"Update task 5 title to 'Buy milk and bread'"**
5. Go to tasks page → Verify title changed ✓
6. Check logs → Should see "update_task succeeded" ✓

#### Test Scenario 2: Update Priority
1. Say: **"Change task 5 priority to high"**
2. Go to tasks page → Verify badge is now red/high ✓
3. Check logs → Should see "update_task: Successfully committed" ✓

#### Test Scenario 3: Delete Task
1. Say: **"Delete task 5"**
2. Go to tasks page → Verify task is gone ✓
3. Check logs → Should see "delete_task: Successfully deleted" ✓

---

## What to Look For

### ✅ Success Indicators
- Test script shows "✓ ALL TESTS PASSED"
- Tasks page reflects changes immediately
- Logs show "Successfully committed" messages
- No errors in console or logs

### ❌ Failure Indicators
- Test script shows "❌ FAILED"
- Tasks page doesn't change
- Logs show "ERROR" or "WARNING"
- Traceback in logs

---

## Troubleshooting

### Issue: Test script fails with "Test user not found"
**Solution:**
```bash
# Create test user
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'
```

### Issue: Database connection error
**Solution:**
Check `.env` file has correct `DATABASE_URL`

### Issue: Import errors
**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

---

## Log Patterns to Expect

### Successful Update
```
INFO - Executing update_task for user user-abc
INFO - update_task: Querying task 5 for user user-abc
INFO - update_task: Found task - id=5, title=Old Title
INFO - update_task: Successfully committed task 5 to database
INFO - update_task succeeded: task_id=5, title=New Title
```

### Successful Delete
```
INFO - Executing delete_task for user user-abc
INFO - delete_task: Querying task 5 for user user-abc
INFO - delete_task: Found task - id=5, title=Buy milk
INFO - delete_task: Successfully deleted task 5 from database
INFO - delete_task succeeded: task_id=5, title=Buy milk
```

### Task Not Found (Expected for wrong ID)
```
WARNING - update_task: Task 999 not found for user user-abc
ERROR - update_task failed for task_id=999: Task not found
```

---

## Testing Checklist

- [ ] Test script passes all 3 tests
- [ ] Update task title works
- [ ] Update task priority works
- [ ] Update task description works
- [ ] Delete task works
- [ ] Changes persist in database
- [ ] Logs show detailed execution trace
- [ ] No errors in console
- [ ] Frontend reflects changes immediately

---

## Files Changed

1. `src/mcp_tools/update_task.py` - Added due_date + logging
2. `src/mcp_tools/delete_task.py` - Added logging
3. `src/routes/chat.py` - Enhanced logging
4. `scripts/test_update_delete.py` - New test script

---

**Time to Test:** ~5 minutes
**Tests:** 3 automated + 3 manual scenarios
**Documentation:** BUGFIX_SUMMARY.md, PHR in history/prompts/general/
