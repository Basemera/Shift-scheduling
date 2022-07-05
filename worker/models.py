from django.db import models
from department.models import Department
from users.models import User
import json
# Create your models here.

class Worker(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self) -> str:
        d = {
            'id': self.id,
            'worker_email': self.user.email,
            'department': self.department.name,
            'manager':self.department.manager.email
        }
        return '%s'% (json.dumps(d, indent = 4, sort_keys = True, default = str))