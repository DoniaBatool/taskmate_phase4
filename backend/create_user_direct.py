#!/usr/bin/env python3
"""Script to create a test user directly in the database."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db import get_session
from src.models import User
from src.auth.password import hash_password
from sqlmodel import select


def create_test_user():
    """Create a test user directly in the database."""
    session = next(get_session())

    try:
        # Check if user already exists
        statement = select(User).where(User.email == "test@example.com")
        existing_user = session.exec(statement).first()

        if existing_user:
            print(f"✅ User already exists: {existing_user.email} (ID: {existing_user.id})")
            return existing_user

        # Create new user
        user = User(
            email="test@example.com",
            password_hash=hash_password("test123"),
            name="Test User"
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        print(f"✅ Test user created successfully!")
        print(f"   Email: {user.email}")
        print(f"   ID: {user.id}")
        print(f"   Name: {user.name}")
        return user

    except Exception as e:
        session.rollback()
        print(f"❌ Error: {str(e)}")
        return None
    finally:
        session.close()


if __name__ == "__main__":
    print("Creating test user...")
    create_test_user()