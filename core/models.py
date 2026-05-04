from django.db import models
from django.contrib.auth.models import User

class UserBank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Account of {self.user.username}"