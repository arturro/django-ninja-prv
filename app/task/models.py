from django.db import models
from django.contrib.auth.models import AbstractUser


class Organization(models.Model):
    """
    Represents a tenant (organization) in the multi-tenant system.
    """
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
     Custom User model with a foreign key to Organization.
     This links a user to exactly one organization.
     """
    organization = models.OneToOneField(
        Organization,
        on_delete=models.CASCADE,
        related_name='user',
        null = True,  # TODO: check this later
        blank = True,  # TODO: check this later
    )


class Task(models.Model):
    """
    Represents a task within an organization.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)

    # Relationships for multi-tenancy and task assignment
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )

    # Task metadata and priority
    created_at = models.DateTimeField(auto_now_add=True)
    deadline_datetime_with_tz = models.DateTimeField()
    priority = models.IntegerField(default=0)

    class Meta:
        ordering = ['deadline_datetime_with_tz', '-priority']

    def __str__(self):
        return self.title

