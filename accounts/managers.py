from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(
        self,
        email: str,
        phone: str,
        password: str,
        first_name: str,
        last_name: str,
        **extra_fields,
    ):
        if not email:
            raise ValueError("email must be entered")
        if not phone:
            raise ValueError("phone must be entered")
        if not first_name:
            raise ValueError("first name must be entered")
        if not last_name:
            raise ValueError("last name must be entered")

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        phone: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        **extra_fields,
    ):
        extra_fields.setdefault("email_verified", False)
        extra_fields.setdefault("is_admin", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(
            phone=phone,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )

    def create_superuser(
        self,
        phone: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        **extra_fields,
    ):
        extra_fields.setdefault("email_verified", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(
            phone=phone,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
