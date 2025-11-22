
from typing import List, Optional
from datetime import datetime
from enum import Enum


class TodoStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


# Priority: 1 (highest) to 5 (lowest)
PRIORITY_MIN = 1
PRIORITY_MAX = 5


class TodoItem:
    def __init__(self, id: str, title: str, description: Optional[str], tags: List[str], status: str, priority: int, created_at: datetime, updated_at: datetime):
        self.id = id
        self.title = title
        self.description = description
        self.tags = tags
        self.status = status
        self.priority = int(priority)
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"<TodoItem {self.id} {self.title} {self.status}>"


class TodoCreate:
    def __init__(self, title: str, description: Optional[str] = None, tags: Optional[List[str]] = None, priority: int = 3):
        self.title = title
        self.description = description
        self.tags = tags or []
        self.priority = int(priority)


class TodoUpdate:
    def __init__(self, title: Optional[str] = None, description: Optional[str] = None, tags: Optional[List[str]] = None, status: Optional[str] = None, priority: Optional[int] = None):
        self.title = title
        self.description = description
        self.tags = tags
        self.status = status
        self.priority = int(priority) if priority is not None else None