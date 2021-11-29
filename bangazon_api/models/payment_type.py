from django.db import models
from django.contrib.auth.models import User


class PaymentType(models.Model):
    merchant_name = models.CharField(max_length=25)
    acct_number = models.CharField(max_length=16)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='payment_types')
