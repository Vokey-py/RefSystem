import string
import random
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.db import models

from .managers import CustomUserManager


class InvitationCode(models.Model):
    code = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return self.code

    @staticmethod
    def generate_code(length=6):
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phoneNumber = models.CharField(max_length=11, unique=True)
    email = models.EmailField(blank=True)
    verification_code = models.CharField(max_length=4, blank=True, null=True)
    verification_code_sent_at = models.DateTimeField(blank=True, null=True)
    invitation_code_self = models.ForeignKey(InvitationCode,
                                             on_delete=models.SET_NULL,
                                             blank=True,
                                             null=True,
                                             related_name='invitation_code_self')
    invitation_code_other = models.ForeignKey(InvitationCode,
                                              on_delete=models.SET_NULL,
                                              null=True,
                                              blank=True,
                                              related_name='invitation_code_other')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Add any other fields you need
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='custom_users'  # Add a unique related_name
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='custom_users'  # Add a unique related_name
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "phoneNumber"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email
