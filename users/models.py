from django.db import models

from django.contrib.auth.models import AbstractUser,UserManager

class MyUserManager(UserManager):

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        extra_fields["role"] = "ADMIN"

        return self._create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    ROLES = (
        ("ADMIN", "ADMIN"),
        ("USER", "USER"),
    )

    role = models.CharField(choices=ROLES, default="USER", max_length=5)
    image = models.ImageField(upload_to="user-images")
    phone_number = models.CharField(max_length=20)

    objects = MyUserManager()

    class Meta:
        db_table = "users"
