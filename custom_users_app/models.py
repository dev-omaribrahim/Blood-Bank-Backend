from django.contrib.auth.models import AbstractUser
from django.db import models

from . import choices


class User(AbstractUser):
    user_role = models.CharField(
        max_length=255,
        choices=choices.USER_ROLE_CHOICES,
        null=False,
        blank=False,
        default=choices.CREATOR_USER,
    )

    class Meta:
        verbose_name = "حساب العامل"
        verbose_name_plural = "حسابات العاملين"
