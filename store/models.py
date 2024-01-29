from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
    c_name = models.CharField(max_length=50, blank=True, null=True)

class Product(models.Model):
    c_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    p_name = models.CharField(max_length=50, blank=True, null=True)
    p_description = models.TextField(max_length=100, blank=True, null=True)

class Staff(models.Model):
    staff_name = models.CharField(max_length=100, blank=True, null=True)
    staff_email = models.EmailField(blank=True, null=True)
    staff_phone = models.CharField(max_length=10, blank=True, null=True)
    staff_section = models.CharField(max_length=50, blank=True, null=True)

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=20, unique=True, editable=False)
    t_date_time = models.DateTimeField(auto_now=True, auto_now_add=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    issued_to_staff = models.ForeignKey(Staff, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    issued_quantity = models.IntegerField(default=0, blank=True, null=True)
    received_quantity = models.IntegerField(default=0, blank=True, null=True)
    balance_quantity = models.IntegerField(default=0, blank=True, null=True)
    # export_to_csv = models.BooleanField(default=False, blank=True, null=True)
