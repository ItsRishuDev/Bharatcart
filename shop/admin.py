from django.contrib import admin
from shop.models import Address, Product, Category, Contact, Cart, OrderDetail

# Register your models here.
admin.site.register(Address)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(Cart)
admin.site.register(OrderDetail)