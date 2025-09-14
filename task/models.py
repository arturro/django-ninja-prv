from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


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
        'tenant.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='tasks',
        help_text="The user assigned to this task.",
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

    def clean(self):
        super().clean()
        if self.assigned_to and self.organization:
            if self.assigned_to.organization != self.organization:
                raise ValidationError(
                    {
                        'assigned_to': "The assigned user must belong to the same organization as the task.",
                        'organization': "The assigned user must belong to the same organization as the task.",
                    }
                )
