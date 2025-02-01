from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([Disease,Hospital,Health_policy,Area,House_policy,Customer,Pending_policies, Approved_policies,House_policies,Pending_house_policies,Approved_house_policies])
