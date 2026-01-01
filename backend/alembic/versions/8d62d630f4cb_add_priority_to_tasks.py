"""add_priority_to_tasks

Revision ID: 8d62d630f4cb
Revises: 3024f0c51bd1
Create Date: 2026-01-01 15:10:48.223035

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d62d630f4cb'
down_revision: Union[str, Sequence[str], None] = '3024f0c51bd1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the enum type
    op.execute("CREATE TYPE priority_enum AS ENUM ('high', 'medium', 'low')")

    # Add the priority column with default value
    op.add_column(
        'tasks',
        sa.Column(
            'priority',
            sa.Enum('high', 'medium', 'low', name='priority_enum'),
            nullable=False,
            server_default='medium'
        )
    )

    # Create composite index for filtering performance
    op.create_index(
        'ix_tasks_user_priority',
        'tasks',
        ['user_id', 'priority']
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the index
    op.drop_index('ix_tasks_user_priority', table_name='tasks')

    # Drop the column
    op.drop_column('tasks', 'priority')

    # Drop the enum type
    op.execute('DROP TYPE priority_enum')
