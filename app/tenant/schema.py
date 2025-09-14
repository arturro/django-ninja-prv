from datetime import datetime
from typing import Annotated
from django.contrib.auth import get_user_model
from ninja import Schema
from pydantic import BeforeValidator, EmailStr


def validate_unique_username(username: str) -> str:
    User = get_user_model()
    if User.objects.filter(username=username).exists():
        raise ValueError(f"User with username '{username}' already exists")
    return username


UserName = Annotated[str, BeforeValidator(validate_unique_username)]


class UserIn(Schema):
    username: UserName
    password: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    # date_joined: datetime
    organization_id: int


class UserOut(Schema):
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    date_joined: datetime
    organization_id: int


class OrganizationIn(Schema):
    name: str


class OrganizationOut(Schema):
    id: int
    name: str
