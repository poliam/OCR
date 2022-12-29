from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Department(models.Model):
	departmentName = models.CharField(max_length=250)
	status = models.CharField(max_length=250, default="active")
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	is_delete = models.BooleanField(default=0)

class Profile(models.Model):
	firstName = models.CharField(max_length=250, null=True, blank=True)
	middleName = models.CharField(max_length=250, null=True, blank=True)
	lastName = models.CharField(max_length=250, null=True, blank=True)
	email = models.CharField(max_length=250, null=True, blank=True)
	contactNumber = models.CharField(max_length=250, null=True, blank=True)
	department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
	status = models.CharField(max_length=250, null=True, default="active")
	userId = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
