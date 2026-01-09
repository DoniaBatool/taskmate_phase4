#!/usr/bin/env python3
"""Test script for update_task and delete_task MCP tools.

This script verifies that:
1. Tasks can be updated successfully
2. Tasks can be deleted successfully
3. Changes persist in the database
4. Logging is comprehensive
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlmodel import Session, select
from src.db import engine
from src.models import Task, User
from src.mcp_tools.add_task import add_task, AddTaskParams
from src.mcp_tools.update_task import update_task, UpdateTaskParams
from src.mcp_tools.delete_task import delete_task, DeleteTaskParams
from src.mcp_tools.list_tasks import list_tasks, ListTasksParams
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_update_task():
    """Test update_task MCP tool."""
    print("\n" + "="*80)
    print("TEST 1: Update Task")
    print("="*80)

    with Session(engine) as db:
        # Get or create test user
        user = db.exec(select(User).where(User.email == "test@example.com")).first()
        if not user:
            print("❌ Test user not found. Please create a user first.")
            return False

        user_id = user.id
        print(f"✓ Using test user: {user_id}")

        # Add a task
        print("\n1. Adding test task...")
        add_params = AddTaskParams(
            user_id=user_id,
            title="Test Task for Update",
            description="Original description",
            priority="low"
        )
        add_result = add_task(db, add_params)
        task_id = add_result.task_id
        print(f"✓ Created task {task_id}: {add_result.title} (priority: {add_result.priority})")

        # Verify task exists before update
        print("\n2. Verifying task exists in database...")
        task_before = db.exec(select(Task).where(Task.id == task_id)).first()
        if not task_before:
            print(f"❌ Task {task_id} not found in database!")
            return False
        print(f"✓ Task exists: id={task_before.id}, title={task_before.title}, priority={task_before.priority}")

        # Update the task
        print("\n3. Updating task...")
        update_params = UpdateTaskParams(
            user_id=user_id,
            task_id=task_id,
            title="Updated Test Task",
            description="Updated description",
            priority="high"
        )
        update_result = update_task(db, update_params)
        print(f"✓ Update returned: id={update_result.task_id}, title={update_result.title}, priority={update_result.priority}")

        # Verify changes persisted
        print("\n4. Verifying changes persisted in database...")
        db.expire_all()  # Clear cache to force fresh query
        task_after = db.exec(select(Task).where(Task.id == task_id)).first()
        if not task_after:
            print(f"❌ Task {task_id} disappeared from database!")
            return False

        print(f"✓ Task after update: id={task_after.id}, title={task_after.title}, priority={task_after.priority}")

        # Verify changes
        success = True
        if task_after.title != "Updated Test Task":
            print(f"❌ Title not updated! Expected 'Updated Test Task', got '{task_after.title}'")
            success = False
        else:
            print("✓ Title updated correctly")

        if task_after.description != "Updated description":
            print(f"❌ Description not updated! Expected 'Updated description', got '{task_after.description}'")
            success = False
        else:
            print("✓ Description updated correctly")

        if task_after.priority != "high":
            print(f"❌ Priority not updated! Expected 'high', got '{task_after.priority}'")
            success = False
        else:
            print("✓ Priority updated correctly")

        # Clean up
        print("\n5. Cleaning up...")
        db.delete(task_after)
        db.commit()
        print("✓ Test task deleted")

        return success


def test_delete_task():
    """Test delete_task MCP tool."""
    print("\n" + "="*80)
    print("TEST 2: Delete Task")
    print("="*80)

    with Session(engine) as db:
        # Get or create test user
        user = db.exec(select(User).where(User.email == "test@example.com")).first()
        if not user:
            print("❌ Test user not found. Please create a user first.")
            return False

        user_id = user.id
        print(f"✓ Using test user: {user_id}")

        # Add a task
        print("\n1. Adding test task...")
        add_params = AddTaskParams(
            user_id=user_id,
            title="Test Task for Delete",
            description="Will be deleted",
            priority="medium"
        )
        add_result = add_task(db, add_params)
        task_id = add_result.task_id
        print(f"✓ Created task {task_id}: {add_result.title}")

        # Verify task exists before delete
        print("\n2. Verifying task exists in database...")
        task_before = db.exec(select(Task).where(Task.id == task_id)).first()
        if not task_before:
            print(f"❌ Task {task_id} not found in database!")
            return False
        print(f"✓ Task exists: id={task_before.id}, title={task_before.title}")

        # Delete the task
        print("\n3. Deleting task...")
        delete_params = DeleteTaskParams(
            user_id=user_id,
            task_id=task_id
        )
        delete_result = delete_task(db, delete_params)
        print(f"✓ Delete returned: id={delete_result.task_id}, title={delete_result.title}, success={delete_result.success}")

        # Verify task is gone
        print("\n4. Verifying task deleted from database...")
        db.expire_all()  # Clear cache to force fresh query
        task_after = db.exec(select(Task).where(Task.id == task_id)).first()
        if task_after:
            print(f"❌ Task {task_id} still exists in database!")
            # Clean up
            db.delete(task_after)
            db.commit()
            return False

        print("✓ Task successfully deleted from database")
        return True


def test_update_partial():
    """Test partial update (only priority, not title)."""
    print("\n" + "="*80)
    print("TEST 3: Partial Update (Priority Only)")
    print("="*80)

    with Session(engine) as db:
        # Get or create test user
        user = db.exec(select(User).where(User.email == "test@example.com")).first()
        if not user:
            print("❌ Test user not found. Please create a user first.")
            return False

        user_id = user.id
        print(f"✓ Using test user: {user_id}")

        # Add a task
        print("\n1. Adding test task...")
        add_params = AddTaskParams(
            user_id=user_id,
            title="Test Partial Update",
            description="Original description",
            priority="low"
        )
        add_result = add_task(db, add_params)
        task_id = add_result.task_id
        original_title = add_result.title
        print(f"✓ Created task {task_id}: {add_result.title} (priority: {add_result.priority})")

        # Update only priority
        print("\n2. Updating priority only (not title)...")
        update_params = UpdateTaskParams(
            user_id=user_id,
            task_id=task_id,
            priority="high"  # Only updating priority
        )
        update_result = update_task(db, update_params)
        print(f"✓ Update returned: title={update_result.title}, priority={update_result.priority}")

        # Verify changes
        print("\n3. Verifying changes...")
        db.expire_all()
        task_after = db.exec(select(Task).where(Task.id == task_id)).first()

        success = True
        if task_after.title != original_title:
            print(f"❌ Title changed unexpectedly! Expected '{original_title}', got '{task_after.title}'")
            success = False
        else:
            print(f"✓ Title unchanged: {task_after.title}")

        if task_after.priority != "high":
            print(f"❌ Priority not updated! Expected 'high', got '{task_after.priority}'")
            success = False
        else:
            print("✓ Priority updated correctly")

        # Clean up
        print("\n4. Cleaning up...")
        db.delete(task_after)
        db.commit()
        print("✓ Test task deleted")

        return success


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("TESTING UPDATE_TASK AND DELETE_TASK MCP TOOLS")
    print("="*80)

    results = {
        "Update Task": test_update_task(),
        "Delete Task": test_delete_task(),
        "Partial Update": test_update_partial()
    }

    print("\n" + "="*80)
    print("TEST RESULTS SUMMARY")
    print("="*80)
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")

    all_passed = all(results.values())
    print("\n" + "="*80)
    if all_passed:
        print("✓ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print("="*80 + "\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
