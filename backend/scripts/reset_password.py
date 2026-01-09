#!/usr/bin/env python3
"""
Script to reset user password.
Usage: python3 scripts/reset_password.py <email> <new_password>
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db import get_session
from src.models import User
from src.auth.password import hash_password
from sqlmodel import select


def reset_password(email: str, new_password: str):
    """Reset password for a user."""
    session = next(get_session())

    try:
        # Find user
        statement = select(User).where(User.email == email.lower())
        user = session.exec(statement).first()

        if not user:
            print(f"❌ User not found: {email}")
            return False

        # Hash new password
        new_hash = hash_password(new_password)

        # Update password
        user.password_hash = new_hash
        session.add(user)
        session.commit()

        print(f"✅ Password reset successful!")
        print(f"   Email: {user.email}")
        print(f"   New Password: {new_password}")
        print(f"\nYou can now login with these credentials.")
        return True

    except Exception as e:
        session.rollback()
        print(f"❌ Error: {str(e)}")
        return False
    finally:
        session.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 scripts/reset_password.py <email> <new_password>")
        print("\nExample:")
        print("  python3 scripts/reset_password.py user@example.com NewPass123")
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2]

    if len(password) < 8:
        print("❌ Password must be at least 8 characters long")
        sys.exit(1)

    print(f"\n🔐 Resetting password for: {email}")
    reset_password(email, password)
