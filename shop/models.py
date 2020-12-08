from django.db import models
from business.models import Business
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=250)
    pincode = models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    
    def __str__(self):
        return self.address
    

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)
    category_img = models.ImageField(upload_to = 'shop/images', default='')
    category_description = models.TextField()

    def __str__(self):
        return self.category_name
    

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_desc = models.TextField()
    product_img_1 = models.ImageField(upload_to = 'shop/images', null=True, blank=True)
    product_img_2 = models.ImageField(upload_to = 'shop/images', null=True, blank=True)
    product_img_3 = models.ImageField(upload_to = 'shop/images', null=True, blank=True)
    product_price = models.IntegerField()
    product_discount = models.IntegerField()
    product_addon = models.DateField(default=datetime.now, blank=True)
    product_category = models.ForeignKey(Category, on_delete = models.CASCADE)
    product_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product_stock = models.IntegerField()

    def __str__(self):
        return self.product_name
    
class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE) 
    prod_id = models.ForeignKey(Product, on_delete = models.CASCADE) 
    quantity = models.IntegerField(default=1)           

    def __str__(self):
        return self.user_id.first_name
    

class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    contact_name = models.CharField(max_length = 100)
    contact_email = models.CharField(max_length = 100)
    contact_number = models.BigIntegerField()
    contact_subject = models.CharField(max_length=100)
    contact_message = models.TextField()

    def __str__(self):
        return self.contact_name    

class OrderDetail(models.Model):
    order_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    email = models.CharField(max_length=100)
    quantity = models.IntegerField()       
    payment_id = models.CharField(max_length=200, default=1)
    paid = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
