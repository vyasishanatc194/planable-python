import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext as _
from planable.models import ActivityTracking
from .common import City
# Create your models here.


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have a valid email address.")

        if not kwargs.get("username"):
            raise ValueError("Users must have a valid username.")

        account = self.model(
            email=self.normalize_email(email), username=kwargs.get("username")
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_superuser = True
        account.is_staff = True
        account.save()

        return account


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(null=True, blank=True, unique=True)
    username = models.CharField(max_length=55, blank=True, null=True,default='')
    full_name = models.CharField(max_length=55, blank=True)
    profile_image = models.ImageField(upload_to="user_profile_image", null=True,  blank=True, verbose_name=_("Profile Image"))
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.ForeignKey("app.City", on_delete=models.CASCADE, related_name="City", null=True, blank=True)

    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name=_("Unique Id"),)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return str(self.email)

    def __unicode__(self):
        return self.pk

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]


class UserProfileImage(ActivityTracking):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_by_user")
    profile_image = models.ImageField(upload_to="profile_images", null=True,  blank=True, verbose_name=_("Profile Image"))

    def __str__(self):
        return f"{self.user.email}"

    class Meta:
        verbose_name = "Creator Review"
        verbose_name_plural = "Creator reviews"
        ordering = ["-created_at"]