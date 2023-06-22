from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    # Add custom fields if needed
    # For example: additional fields like age, phone number, etc.
    age = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Define related_name for groups and user_permissions fields
    groups = models.ManyToManyField(Group, blank=True, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='custom_user_set',
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        related_query_name='custom_user'
    )

    # Add any additional methods or overrides as needed
