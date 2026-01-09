"""MCP Tool: find_task

Finds task by title for the authenticated user with fuzzy matching.

This tool enables AI agents to find task IDs based on
natural language task titles, with smart fuzzy matching for better results.
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from sqlmodel import Session, select
import logging

from ..models import Task
from ..ai_agent.utils import fuzzy_match_task_title

logger = logging.getLogger(__name__)


class FindTaskParams(BaseModel):
    """Input parameters for find_task tool.

    Attributes:
        user_id: ID of the authenticated user (for isolation)
        title: Task title to search for
    """

    user_id: str = Field(..., description="User ID for task ownership")
    title: str = Field(..., description="Task title to search for")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "user_id": "user-123",
                "title": "buy book"
            }
        }


class FindTaskResult(BaseModel):
    """Result from find_task tool execution.

    Attributes:
        task_id: ID of the found task (or null if not found)
        title: Task title
        description: Task description
        completed: Task completion status
        priority: Task priority level
        created_at: Timestamp when task was created
        confidence_score: Fuzzy match confidence (0-100)
    """

    task_id: int = Field(..., description="ID of the task")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    completed: bool = Field(..., description="Task completion status")
    priority: str = Field(..., description="Task priority level")
    created_at: str = Field(..., description="Timestamp of creation")
    confidence_score: int = Field(..., description="Fuzzy match confidence (0-100)")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "task_id": 3,
                "title": "buy book",
                "description": "From bookstore",
                "completed": False,
                "priority": "medium",
                "created_at": "2025-12-30T16:30:00Z",
                "confidence_score": 95
            }
        }


def find_task(db: Session, params: FindTaskParams) -> Optional[FindTaskResult]:
    """Find task by title for the authenticated user with fuzzy matching.

    This is the core MCP tool function that AI agents call to find tasks by title.
    Uses intelligent fuzzy matching to handle typos, partial matches, and natural language.

    Args:
        db: Database session
        params: Task search parameters

    Returns:
        FindTaskResult with task details if found, None if not found

    Security:
        - Enforces user isolation: query filters by user_id
        - Fuzzy matching with confidence threshold

    Example:
        >>> params = FindTaskParams(
        ...     user_id="user-123",
        ...     title="buy book"  # Can match "Buy books", "by book", etc.
        ... )
        >>> result = find_task(db, params)
        >>> if result:
        ...     print(f"Found task {result.task_id}: {result.title} ({result.confidence_score}% match)")
    """
    logger.info(f"find_task: Searching for '{params.title}' for user {params.user_id}")

    # Fetch all user's tasks for fuzzy matching
    query = select(Task).where(Task.user_id == params.user_id)

    try:
        tasks = db.exec(query).all()
    except Exception as e:
        logger.error(f"find_task: Database error: {e}", exc_info=True)
        raise RuntimeError(f"Failed to query tasks: {str(e)}") from e

    # Handle no tasks
    if not tasks:
        logger.info(f"find_task: User {params.user_id} has no tasks")
        return None

    logger.info(f"find_task: Found {len(tasks)} tasks for user {params.user_id}")

    # Create title mapping for fuzzy matching
    task_map = {task.title: task for task in tasks}
    task_titles = list(task_map.keys())

    # Perform fuzzy matching
    matches = fuzzy_match_task_title(params.title, task_titles, threshold=60)

    # Handle no matches
    if not matches:
        logger.info(f"find_task: No fuzzy matches found for '{params.title}'")
        return None

    # Get best match (highest score)
    best_match_title, confidence_score = matches[0]
    task = task_map[best_match_title]

    logger.info(
        f"find_task: Best match - task_id={task.id}, title='{task.title}', "
        f"confidence={confidence_score}%"
    )

    # Return result with confidence score
    return FindTaskResult(
        task_id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        priority=task.priority,
        created_at=task.created_at.isoformat() if task.created_at else None,
        confidence_score=confidence_score
    )