from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Disease(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Hospital(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=100)
    diseases = models.ManyToManyField(Disease)

    def __str__(self):
        return f"{self.name}"

class Health_policy(models.Model):
    policy_id = models.CharField(max_length=100)
    premium = models.IntegerField()
    tenure = models.IntegerField()
    covered_illnesses = models.ManyToManyField(Disease)
    covered_hospitals = models.ManyToManyField(Hospital)

    def __str__(self):
        return self.policy_id

class Area(models.Model):
    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField(default=1000)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} "

class House_policy(models.Model):
    tenure = models.IntegerField(default=12)
    area = models.ManyToManyField(Area)

    def __str__(self):
        return self.policy_id

class Customer(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    phone = models.PositiveIntegerField()
    address = models.CharField(max_length=200)
    health_policies = models.ManyToManyField(Health_policy,blank=True,null=True)
    house_policies = models.ManyToManyField(House_policy,blank=True,null=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100,default='Pending')
    

class Pending_policies(models.Model):
    policy = models.OneToOneField(Customer,on_delete=models.CASCADE)

class Approved_policies(models.Model):
    policy = models.OneToOneField(Customer,on_delete=models.CASCADE)

class House_policies(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    location = models.ForeignKey(Area,  on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100,default='Pending')


class Pending_house_policies(models.Model):
    policy = models.OneToOneField(House_policies,on_delete=models.CASCADE)

class Approved_house_policies(models.Model):
    policy = models.OneToOneField(House_policies,on_delete=models.CASCADE)