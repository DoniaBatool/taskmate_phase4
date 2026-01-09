#!/usr/bin/env python3
"""Quick test script to verify the chat endpoint fix."""

import requests
import jwt
import time
from datetime import datetime, timedelta

# Environment variables (same as .env)
SECRET_KEY = "cZ5X2KOKa8tGazYO73qISjBBautFLi7j"
ALGORITHM = "HS256"

def create_test_token(user_id="test-user-123"):
    """Create a test JWT token."""
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(days=1),
        "iat": datetime.utcnow(),
        "user_id": user_id
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def test_chat_endpoint():
    """Test the chat endpoint with list tasks."""
    user_id = "test-user"  # Match the path parameter
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

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            result = response.json()
            print(f"\nAgent Response: {result['response']}")
            print(f"Tool Calls: {result['tool_calls']}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_chat_endpoint()