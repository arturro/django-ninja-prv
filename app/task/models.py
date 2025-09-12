from django.contrib.auth.models import AbstractUser
from django.db import models


# class Organization(models.Model):
#     """
#     Represents a tenant or organization in the multi-tenant system.
#     Each user and task belongs to a single organization.
#     """
#
#     name = models.CharField(max_length=255, unique=True, help_text="The name of the organization.")
#     created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time the organization was created.")
#
#     def __str__(self):
#         return self.name
#
#
# class User(AbstractUser):
#     """
#     Custom user model with a foreign key to an organization.
#     This links each user to a specific tenant.
#     """
#
#     organization = models.ForeignKey(
#         'Organization',
#         on_delete=models.CASCADE,
#         related_name='users',
#         help_text="The organization this user belongs to.",
#         null=True,  # TODO: Consider whether this should be nullable.
#         blank=True,
#     )
#
#     def __str__(self):
#         return self.username


class Task(models.Model):
    """
    Represents a task within a specific organization.
    Tasks are assigned to a user within the same organization.
    """

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=255, help_text="The title of the task.")
    description = models.TextField(blank=True, help_text="A detailed description of the task.")
    completed = models.BooleanField(default=False, help_text="Indicates if the task is completed.")

    assigned_to = models.ForeignKey(
        'tenant.User', on_delete=models.SET_NULL, null=True, related_name='tasks', help_text="The user assigned to this task."
    )

    organization = models.ForeignKey(
        'tenant.Organization',
        on_delete=models.CASCADE,
        related_name='tasks',
        help_text="The organization this task belongs to.",
    )

    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time the task was created.")

    deadline_datetime_with_tz = models.DateTimeField(
        help_text="The deadline for the task, including timezone information."
    )

    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default='medium', help_text="The priority level of the task."
    )

    class Meta:
        # A Meta class is a good practice for Django models.
        # It allows for model-specific configuration.
        # This will order tasks by their deadline and priority by default.
        ordering = ['deadline_datetime_with_tz', 'priority']

    def __str__(self):
        return self.title
