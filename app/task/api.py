from typing import List

from django.shortcuts import get_object_or_404

from ninja import Router

from .models import Task
from .schema import TaskIn, TaskOut

router = Router()


@router.post("/")
def create_task(request, payload: TaskIn):
    # confirm the user is assigning the task to themselves and within their organization
    if payload.assigned_to_id != request.auth.id:
        return {"error": "You can only assign tasks to yourself."}
    if payload.organization_id != request.auth.organization.id:
        return {"error": "You can only create tasks within your organization."}

    task = Task.objects.create(**payload.dict())
    return {"id": task.id}


@router.get("/", response=List[TaskOut])
def list_tasks(request):
    """
    Retrieve a list of all tasks.
    """
    tasks = Task.objects.select_related("assigned_to", "organization").filter(organization=request.auth.organization)
    return tasks


@router.get("/{task_id}", response=TaskOut)
def get_task(request, task_id: int):
    """
    Get a specific task by its ID.
    """
    task = get_object_or_404(Task, id=task_id, organization=request.auth.organization)
    return task
