from datetime import datetime
from typing import Optional

from ninja import Schema


class TaskOut(Schema):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    priority: str
    # assigned_to: UserOut
    assigned_to_id: int
    organization_id: int  # Organization ID
    # organization: OrganizationOut
    created_at: datetime
    deadline_datetime_with_tz: datetime

    class Config:
        from_attributes = True


class TaskIn(Schema):
    # id: int
    title: str
    description: Optional[str]
    completed: bool
    priority: str
    assigned_to_id: int
    organization_id: int
    deadline_datetime_with_tz: datetime

    class Config:
        from_attributes = True
