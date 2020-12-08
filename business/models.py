from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Business(models.Model):
    business_id = models.AutoField(primary_key=True)
    business_name = models.CharField(max_length=100)
    credential = models.ForeignKey(User, on_delete=models.CASCADE)
    seller_name = models.CharField(max_length=100)
    business_mobile = models.BigIntegerField()
    business_email = models.CharField(max_length=50)
    servicable_area = models.IntegerField()
    service_discription = models.TextField()
    delivery_avail = models.BooleanField(default=False)
    # business_image = models.ImageField(upload_to = 'business', default = '')

    def __str__(self):
        return self.business_name
    