from django.contrib.auth.models import User
from django.db import models
import uuid
# Create your models here.


class Category(models.Model):
    c_name = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.c_name


class Product(models.Model):
    c_name = models.ForeignKey(Category, on_delete=models.PROTECT)
    p_name = models.CharField(max_length=100, blank=True, null=True)
    p_description = models.TextField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    def __str__(self):
        return self.p_name + "    " + str(self.c_name) + "    " + self.p_description + "    " + str(self.quantity)


class Staff(models.Model):
    staff_name = models.CharField(max_length=100, blank=True, null=True)
    staff_email = models.EmailField(blank=True, null=True)
    staff_phone = models.CharField(max_length=10, blank=True, null=True)
    staff_section = models.CharField(max_length=100, blank=True, null=True)


class Section(models.Model):
    section_name = models.CharField(max_length=100, blank=True, null=True)


class Transaction(models.Model):
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    t_date_time = models.DateTimeField(auto_now=True, auto_now_add=False)
    product = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    issued_to = models.CharField(max_length=100, blank=True, null=True)
    user = models.CharField(max_length=100, blank=True, null=True)
    issued_quantity = models.IntegerField(default=0, blank=True, null=True)
    received_quantity = models.IntegerField(default=0, blank=True, null=True)
    received_from = models.CharField(max_length=100, blank=True, null=True)


class Recipient(models.Model):
    rec_name = models.CharField(max_length=100, blank=True, null=True)
    rec_quantity = models.IntegerField(default=0, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)


class Request_Items(models.Model):
    tracking_id = models.CharField(max_length=100, blank=True, null=True)
    product_name = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_time = models.DateTimeField(auto_now=True, auto_now_add=False)
    is_accepted = models.BooleanField(default=False, blank=True, null=True)
