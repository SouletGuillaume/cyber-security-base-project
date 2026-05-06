from django.db import models
from django.contrib.auth.models import User

class UserBank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Account of {self.user.username}"

class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    # used for flaw 4, to simulate the storage of sensitive financial identifiers in plain text in the database
    receiver_iban = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)