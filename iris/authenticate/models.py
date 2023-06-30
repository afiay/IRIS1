from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.urls import reverse

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='media/user_profile_pictures/', blank=True, null=True)
    cover_picture = models.ImageField(upload_to='media/user_cover_pictures/', blank=True, null=True)
    joined_date = models.DateTimeField(default=timezone.now, null=True)
    bio = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    groups = models.ManyToManyField(Group, blank=True, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='custom_user_set',
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        related_query_name='custom_user'
    )

    following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='followers')
    is_accepted = models.BooleanField(default=False)

    # Add any additional fields or methods as needed

