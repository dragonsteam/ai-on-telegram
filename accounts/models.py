from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    UserManager as BaseUserManager
)


class UserManager(BaseUserManager):
    def _create_user(self, telegram_id, password, **extra_fields):
        # if not email:
        #     raise ValueError("The given email must be set")
        # email = self.normalize_email(email)
        
        user = self.model(telegram_id=telegram_id, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, telegram_id, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(telegram_id, password, **extra_fields)


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=255, verbose_name="First name")
    last_name = models.CharField(max_length=255, verbose_name="Last name")
    # email = models.EmailField(
    # 	"email",
    # 	unique=True,
    # 	error_messages={
    # 		"unique": "A user with this email already exists.",
    # 	},
    # )
    telegram_id = models.BigIntegerField(
        "telegram_id",
        unique=True,
        error_messages={
            "unique": "A user with this telegram id already existx",
        }
    )

    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} {self.telegram_id}"
        # return self.phone.as_international