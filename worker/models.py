from django.db import models
from department.models import Department
from users.models import User
# Create your models here.

class Worker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=False, null=False)