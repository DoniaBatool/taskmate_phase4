"""MCP Tool: add_task

Creates a new task for the authenticated user.

This tool enables AI agents to add tasks to a user's todo list based on
natural language input.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator
from sqlmodel import Session
import logging

from ..models import Task
from ..ai_agent.utils import parse_natural_date

logger = logging.getLogger(__name__)


class AddTaskParams(BaseModel):
    """Input parameters for add_task tool.

    Attributes:
        user_id: ID of the authenticated user (for isolation)
        title: Task title (1-200 characters)
        description: Optional task description
        priority: Task priority level (high, medium, low) - defaults to medium
        due_date: Optional due date in natural language (e.g., 'tomorrow', 'next Friday at 3pm', '2026-01-15')
    """

    user_id: str = Field(..., description="User ID for task ownership")
    title: str = Field(..., description="Task title (1-200 characters)")
    description: Optional[str] = Field(None, description="Optional task description")
    priority: str = Field(
        default="medium",
        description="Task priority level (high, medium, low)"
    )
    due_date: Optional[str] = Field(
        None,
        description="Due date in natural language (e.g., 'tomorrow', 'next Friday at 3pm', 'January 15', '2026-01-15T14:30:00')"
    )

    @validator("priority")
    def validate_priority(cls, v):
        """Validate priority is one of the allowed values."""
        allowed = ["high", "medium", "low"]
        if v not in allowed:
            raise ValueError(
                f"Invalid priority: {v}. Must be one of: {', '.join(allowed)}"
            )
        return v

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "user_id": "user-123",
                "title": "Buy milk",
                "description": "Get 2% milk from grocery store",
                "priority": "high",
                "due_date": "tomorrow at 5pm"
            }
        }


class AddTaskResult(BaseModel):
    """Result from add_task tool execution.

    Attributes:
        task_id: ID of the created task
        title: Task title
        description: Task description (if provided)
        completed: Task completion status (always False for new tasks)
        priority: Task priority level (high, medium, low)
        due_date: Task due date and time (if provided)
        created_at: Timestamp when task was created
    """

    task_id: int = Field(..., description="ID of the created task")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    completed: bool = Field(False, description="Task completion status")
    priority: str = Field(..., description="Task priority level")
    due_date: Optional[datetime] = Field(None, description="Task due date and time")
    created_at: datetime = Field(..., description="Task creation timestamp")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "task_id": 42,
                "title": "Buy milk",
                "description": "Get 2% milk from grocery store",
                "completed": False,
                "priority": "high",
                "due_date": "2026-01-10T17:00:00Z",
                "created_at": "2025-12-30T10:30:00Z"
            }
        }


def add_task(db: Session, params: AddTaskParams) -> AddTaskResult:
    """Create a new task for the user.

    This is the core MCP tool function that AI agents call to add tasks.

    Args:
        db: Database session
        params: Task creation parameters

    Returns:
        AddTaskResult with created task details

    Raises:
        ValueError: If validation fails (empty title, title too long)

    Example:
        >>> params = AddTaskParams(
        ...     user_id="user-123",
        ...     title="Buy milk",
        ...     description="Get 2% milk"
        ... )
        >>> result = add_task(db, params)
        >>> assert result.task_id > 0
        >>> assert result.title == "Buy milk"
    """
    # Validate title
    title = params.title.strip() if params.title else ""

    if not title:
        raise ValueError("Title cannot be empty")

    if len(title) > 200:
        raise ValueError("Title must be 200 characters or less")

    # Parse due_date if provided
    parsed_due_date = None
    if params.due_date:
        try:
            parsed_due_date = parse_natural_date(params.due_date)
            if parsed_due_date:
                logger.info(f"Parsed due date '{params.due_date}' to {parsed_due_date}")
            else:
                logger.warning(f"Failed to parse due date: '{params.due_date}'")
        except Exception as e:
            logger.error(f"Error parsing due date '{params.due_date}': {e}")
            # Continue without due_date rather than failing the entire request

    # Create task with user isolation
    task = Task(
        user_id=params.user_id,
        title=title,
        description=params.description,
        priority=params.priority,
        due_date=parsed_due_date,
        completed=False,
        created_at=datetime.utcnow()
    )

    # Persist to database
    try:
        db.add(task)
        db.commit()
        db.refresh(task)
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Failed to create task: {str(e)}") from e

    # Return result
    return AddTaskResult(
        task_id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        priority=task.priority,
        due_date=task.due_date,
        created_at=task.created_at
    )
