from operator import mod
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    custom_id=models.AutoField(primary_key=True,unique=True)
    our_user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=80, null=True, blank=True)
    desc=models.CharField(max_length=40, null=True, blank=True)
    upload=models.ImageField(upload_to="uploads/image", null=True, blank=True)

    def __str__(self):
        return self.title
    