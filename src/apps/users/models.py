from allauth.account.models import EmailAddress
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext as _


class UserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
            Create and save a user with the given username, email, and password.
        """

        if not username:
            raise ValueError(_("The given username must be set"))

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        try:
            EmailAddress.objects.create(
                user=user, email=email, primary=True, verified=True
            )
        except Exception as e:
            print(f"UserManager _create_user: {e}")

        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.username}"
