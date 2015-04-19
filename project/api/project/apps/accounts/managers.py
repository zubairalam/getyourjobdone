import uuid

from django.utils import timezone
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext as _


class CustomUserManager(BaseUserManager):
    """
    Custom User Manager
    """

    def create_user(self, email,password=None, **extra_fields):
        """
        Creates and saves a normal User with the given email and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))
        now = timezone.now()
        user = self.model(email=CustomUserManager.normalize_email(email), 
            is_superuser=False, is_staff=False, active=False, last_login=now, hash=uuid.uuid1(),
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,password=None, **extra_fields):
        """
        Creates and saves a Super User(Admin Rights) with the given email and password.
        """
        user = self.create_user(email, password=password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.active = True
        user.save(using=self._db)
        return user
