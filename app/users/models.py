import uuid
import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """

        if not email:
            raise ValueError("Email address must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, *extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the email and password.
        """

        if not email:
            raise ValueError("Email address must be set")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)

    # booleans
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # dates
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(blank=True, null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='custom_user_set_groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='custom_user_set_permissions',
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["date_of_birth"]

    def _str_(self):
        return self.email

    @property
    def age(self):
        if self.birthday:
            age = datetime.date.today() - datetime.date(
                year=self.date_of_birth.year, month=self.date_of_birth.month, day=self.date_of_birth.day
            )
            return int(age.total_seconds() / 31536000.0)
        return None
    
    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)


def file_upload_path(instance, filename):
    # Define the upload path for the file field
    return f'user_{instance.user.id}/{filename}'


class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    title = models.CharField(max_length=255)
    description = models.TextField()
    file_field = models.FileField(upload_to=file_upload_path)

    def __str__(self):
        return self.title
