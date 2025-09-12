from typing import List, Optional

from ninja import Router, Schema
from ninja_jwt.authentication import JWTAuth

from .models import Task

router = Router()


class TaskSchema(Schema):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    priority: str
    assigned_to: Optional[int]  # User ID
    organization: int  # Organization ID
    created_at: str  # ISO format date-time
    deadline_datetime_with_tz: str  # ISO format date-time with timezone

    class Config:
        from_attributes = True


@router.get("/tasks", response=List[TaskSchema], tags=["Tasks"], auth=JWTAuth())
def list_tasks(request):
    """
    Retrieve a list of all tasks.
    """
    tasks = Task.objects.all()
    return tasks
