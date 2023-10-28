import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.urls import reverse

#
from .validators import strongPassword, is_tunisian_phone_number


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(
        max_length=128, validators=[strongPassword], blank=False, null=False
    )
    gender = models.CharField(
        max_length=1,
        choices=[
            ("M", "Male"),
            ("F", "Female"),
        ],
        blank=False,
        null=False,
    )
    phone_number = models.CharField(
        max_length=8,
        blank=False,
        null=False,
        validators=[is_tunisian_phone_number],
        unique=True,
    )

    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)

    REQUIRED_FIELDS = ["email", "first_name", "last_name", "gender", "phone_number"]

    @property
    def is_admin(self):
        return self.account.role == "admin" if hasattr(self, "account") else False

    @property
    def is_member(self):
        return self.account.role == "member" if hasattr(self, "account") else False

    def __str__(self):
        return self.username


class Account(models.Model):
    ROLE_CHOICES = (
        ("user", "User"),
        ("admin", "Admin"),
        ("member", "Member"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        "CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="account",
    )
    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        blank=False,
        null=False,
        default=ROLE_CHOICES[0][0],
    )
    photo = models.ImageField(
        upload_to=settings.ACCOUNTS_PHOTOS_DIR, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_photo_url(self):
        if self.photo:
            return settings.API_BASE_URL + reverse(
                "account-photo-detail", args=[str(self.id)]
            )
        return settings.DEFAULT_ACCOUNT_PHOTO_URL

    def setToMember(self):
        if not self.role in ["admin", "member"]:
            self.role = "member"
            self.save()

    def unsetMember(self):
        if not self.role == "admin":
            self.role = "user"
            self.save()

    def __str__(self):
        return "@" + self.user.username


class JoinClubForm(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.OneToOneField(
        "Account", blank=False, related_name="join_club_form", on_delete=models.CASCADE
    )
    how_found_us = models.CharField(max_length=255, blank=False, null=False)
    reasons = models.CharField(max_length=255, blank=False, null=False)
    goals = models.TextField(max_length=1024, blank=False, null=False)
    receive_emails = models.BooleanField(default=False, blank=True, null=False)
    status = models.CharField(
        max_length=8,
        default=STATUS_CHOICES[0][0],
        blank=True,
        null=False,
        choices=STATUS_CHOICES,
    )

    def accept(self):
        if self.status != self.STATUS_CHOICES[1][0]:
            self.status = self.STATUS_CHOICES[1][0]
            self.account.setToMember()
            self.save()

    def reject(self):
        if self.status != self.STATUS_CHOICES[2][0]:
            self.status = self.STATUS_CHOICES[2][0]
            self.account.unsetMember()
            self.save()

    def __str__(self):
        return str(self.account) + " * Joining Form"
