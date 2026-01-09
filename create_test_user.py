#!/usr/bin/env python3
"""Quick test script to create a test user and verify the chat endpoint fix."""

import requests
import jwt
import time
from datetime import datetime, timedelta

# Environment variables (same as .env)
SECRET_KEY = "cZ5X2KOKa8tGazYO73qISjBBautFLi7j"
ALGORITHM = "HS256"

def create_test_token(user_id="a1b8809b-6e7f-4733-96ef-ebd9aa830c1d"):
    """Create a test JWT token."""
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(days=1),
        "iat": datetime.utcnow(),
        "user_id": user_id
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def create_test_user(user_id="test-user"):
    """Create a test user via the signup endpoint."""
    signup_data = {
        "email": "test@example.com",
        "password": "test123",
        "name": "Test User"
    }

    try:
        response = requests.post(
            "http://localhost:8000/auth/signup",
            json=signup_data,
            timeout=10
        )

        print(f"Signup Status Code: {response.status_code}")
        print(f"Signup Response: {response.text}")

        return response.status_code == 201

    except Exception as e:
        print(f"Signup Error: {e}")
        return False

def test_chat_endpoint(user_id="a1b8809b-6e7f-4733-96ef-ebd9aa830c1d"):
    """Test the chat endpoint with list tasks."""
    token = create_test_token(user_id)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Test message
    data = {
        "message": "list all tasks"
    }

    try:
        response = requests.post(
            f"http://localhost:8000/api/{user_id}/chat",
            json=data,
            headers=headers,
            timeout=10
        )

        print(f"Chat Status Code: {response.status_code}")
        print(f"Chat Response: {response.text}")

        if response.status_code == 200:
            result = response.json()
            print(f"\nAgent Response: {result['response']}")
            print(f"Tool Calls: {result['tool_calls']}")
            return True

    except Exception as e:
        print(f"Chat Error: {e}")

    return False

def test_add_task_first(user_id="a1b8809b-6e7f-4733-96ef-ebd9aa830c1d"):
    """Test adding a task first, then listing."""
    token = create_test_token(user_id)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # First, try to add a task
    add_data = {
        "message": "Add a task to buy milk"
    }

    try:
        response = requests.post(
            f"http://localhost:8000/api/{user_id}/chat",
            json=add_data,
            headers=headers,
            timeout=10
        )

        print(f"Add Task Status Code: {response.status_code}")
        print(f"Add Task Response: {response.text}")

        if response.status_code == 200:
            result = response.json()
            print(f"Add Task Agent Response: {result['response']}")
            print(f"Add Task Tool Calls: {result['tool_calls']}")

        # Now try to list tasks
        list_data = {
            "message": "list all tasks"
        }

        response = requests.post(
            f"http://localhost:8000/api/{user_id}/chat",
            json=list_data,
            headers=headers,
            timeout=10
        )

        print(f"List Tasks Status Code: {response.status_code}")
        print(f"List Tasks Response: {response.text}")

        if response.status_code == 200:
            result = response.json()
            print(f"List Tasks Agent Response: {result['response']}")
            print(f"List Tasks Tool Calls: {result['tool_calls']}")
            return True

    except Exception as e:
        print(f"Task Test Error: {e}")

    return False

if __name__ == "__main__":
    print("=== Testing Chat Endpoint (List Tasks) ===")
    test_chat_endpoint()

    print("\n=== Testing Add Task Then List ===")
    test_add_task_first()