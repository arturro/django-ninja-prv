from typing import List

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from ninja import Router

from tenant.models import User

from .models import Task
from .schema import TaskIn, TaskOut

router = Router()


@router.post("/")
def create_task(request, payload: TaskIn):
    # confirm the user is assigning the task to themselves and within their organization
    if payload.assigned_to_id != request.auth.id:
        assigned_user = get_object_or_404(User, id=payload.assigned_to_id)
        if assigned_user.organization_id != request.auth.organization.id:
            # 403 Forbidden or 404 Not Found?
            return HttpResponse({"error": "You can only assign tasks to your organization."}, status=403)
    if payload.organization_id != request.auth.organization.id:
        # 403 Forbidden or 404 Not Found?
        return HttpResponse({"error": "You can only create tasks within your organization."}, status=403)

    task = Task.objects.create(**payload.dict())
    return {"id": task.id}  # TODO: should return 201 created


@router.get("/", response=List[TaskOut])
def list_tasks(request):
    """
    Retrieve a list of all tasks.
    """
    # TODO: pagination, sorting, filtering
    tasks = Task.objects.select_related("assigned_to", "organization").filter(organization=request.auth.organization)
    return tasks


@router.get("/{task_id}", response=TaskOut)
def get_task(request, task_id: int):
    """
    Get a specific task by its ID.
    """
    task = get_object_or_404(Task, id=task_id, organization=request.auth.organization)
    return task


@router.put("/{task_id}")
def update_task(request, task_id: int, payload: TaskIn):
    task = get_object_or_404(Task, id=task_id, organization=request.auth.organization)
    # confirm the user is assigning the task to themselves and within their organization
    if payload.assigned_to_id != request.auth.id:
        assigned_user = get_object_or_404(User, id=payload.assigned_to_id)
        if assigned_user.organization_id != request.auth.organization.id:
            # 403 Forbidden or 404 Not Found?
            return HttpResponse({"error": "You can only assign tasks to your organization."}, status=403)

    if payload.organization_id != request.auth.organization.id:
        # 403 Forbidden or 404 Not Found?
        return HttpResponse({"error": "You can only create tasks within your organization."}, status=403)

    for attr, value in payload.dict().items():
        setattr(task, attr, value)
    task.save()
    return {"success": True}


@router.delete("/{task_id}")
def delete_task(request, task_id: int):
    task = get_object_or_404(Task, id=task_id, organization=request.auth.organization)
    task.delete()
    return {"success": True}


# TODO: consider add patch endpoint to update only certain fields
