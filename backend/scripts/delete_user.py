#!/usr/bin/env python3
"""Delete user without password_hash from database."""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select
from src.db import engine
from src.models import User


def delete_user_without_password(email: str) -> bool:
    """
    Delete user with no password_hash.

    Args:
        email: User email to delete

    Returns:
        bool: True if user was deleted, False if not found
    """
    with Session(engine) as session:
        # Find user
        statement = select(User).where(User.email == email.lower())
        user = session.exec(statement).first()

        if not user:
            print(f"❌ User not found: {email}")
            return False

        if user.password_hash:
            print(f"⚠️  User has password_hash, not deleting for safety: {email}")
            print(f"   User ID: {user.id}")
            return False

        # Delete user (cascade will delete related tasks/conversations/messages)
        session.delete(user)
        session.commit()

        print(f"✅ Deleted user: {email}")
        print(f"   User ID: {user.id}")
        print(f"   Created: {user.created_at}")
        return True


if __name__ == "__main__":
    # Delete the problematic test user
    email = "test@example.com"
    print(f"🔧 Deleting user without password_hash: {email}")
    print("-" * 50)

    success = delete_user_without_password(email)

    if success:
        print("-" * 50)
        print("✅ User deletion complete!")
        print("\nNow you can signup with this email again.")
    else:
        print("-" * 50)
        print("❌ User deletion failed or not needed.")
        sys.exit(1)
