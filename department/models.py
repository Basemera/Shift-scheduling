from django.db import models

from users.models import User

# Create your models here.

class Department(models.Model):
    name = models.CharField('department_name', max_length=180)
    manager = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null=False)
