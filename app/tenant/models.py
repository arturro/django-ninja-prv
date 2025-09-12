from django.contrib.auth.models import AbstractUser
from django.db import models


class Organization(models.Model):
    """
    Represents a tenant or organization in the multi-tenant system.
    Each user and task belongs to a single organization.
    """

    name = models.CharField(max_length=255, unique=True, help_text="The name of the organization.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time the organization was created.")

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Custom user model with a foreign key to an organization.
    This links each user to a specific tenant.
    """

    organization = models.ForeignKey(
        'Organization',
        on_delete=models.CASCADE,
        related_name='users',
        help_text="The organization this user belongs to.",
        null=True,  # TODO: Consider whether this should be nullable.
        blank=True,
    )

    def __str__(self):
        return self.username