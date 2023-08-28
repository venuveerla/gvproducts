from django.db import models
import datetime
# Create your models here.
class insertdata(models.Model):
    sno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    father=models.CharField(max_length=100)
    village=models.CharField(max_length=100)
    mandal=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    phno1=models.CharField(max_length=100)
    phno2=models.CharField(max_length=100)
    balance=models.IntegerField()
    class Meta:
        db_table='registration'
class addproduct(models.Model):
    pid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    ptype=models.CharField(max_length=100)
    price=models.IntegerField()
    class Meta:
        db_table='productdetails'
class farmerproducts(models.Model):
    pid=models.AutoField(primary_key=True)
    phno=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    quantity=models.IntegerField()
    date=models.DateField()
    billgenerate=models.IntegerField()
    class Meta:
        db_table='farmerpurchase'

