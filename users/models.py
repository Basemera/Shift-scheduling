from enum import Enum
from django.db import models
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):

    class UserTypeChoice(Enum):
        Admin = 1
        Supervisor = 2
        Worker = 3

        @classmethod
        def choices(cls):
            print(tuple((i.name, i.value) for i in cls))
            return [(i.name, i.value) for i in cls]

    choices = ['admin', 'supervisor', 'worker']

    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    nin = models.CharField('nin', max_length=30, blank=True, unique=True)
    phone_number = PhoneNumberField('phone number', blank=True, unique=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    is_active = models.BooleanField('active', default=True)
    # user_type = models.Choices(value=((i.name, i.value) for i in UserTypeChoice))
    user_type = models.CharField(max_length=300, choices=UserTypeChoice.choices())


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_user_type(self):
        '''
        Returns the user type
        '''
        return self.user_type
    
    def is_supervisor_or_admin(self):
        return self.user_type == 'Admin' or self.get_user_type == 'Supervisor'

