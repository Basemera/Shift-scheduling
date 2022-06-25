from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
class UserManager(BaseUserManager):
    
    use_in_migrations: bool = True

    def _create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The email must be given")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        # print(password)
        # hashed_password = make_password(password)
        # print(hashed_password)
        user.set_password(password)
        user.save(using=self._db)
        print(user)
        return user

    def create(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
