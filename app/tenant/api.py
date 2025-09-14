from typing import List

from ninja import Router

from .models import User
from .schema import UserIn, UserOut

router = Router()


@router.post("/")
def create_user(request, payload: UserIn):
    data = payload.dict()
    user = User.objects.create(**data)
    user.set_password(data['password'])
    user.save()
    return {"id": user.id}  # TODO: should return 201 created


@router.get("/", response=List[UserOut])
def list_users(request):
    """
    Retrieve a list of all tasks.
    """
    # TODO: pagination, sorting, filtering
    users = User.objects.filter(organization=request.auth.organization).order_by('last_name', 'first_name')
    return users
