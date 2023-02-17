from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class document_type(models.Model):
	name = models.CharField(max_length=250)
	is_delete = models.BooleanField(default=0)

class document_file(models.Model):
	name = models.CharField(max_length=250, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	docType = models.ForeignKey(document_type, on_delete=models.SET_NULL, null=True, blank=True)
	documentController = models.CharField(max_length=250, null=True, blank=True)
	docFileType = models.CharField(max_length=250)
	filePath = models.CharField(max_length=250, blank=True, null=True)
	docOwner = models.ForeignKey('personnel.Department', on_delete=models.SET_NULL, null=True, blank=True)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	is_delete = models.BooleanField(default=0)
	is_archived = models.BooleanField(default=0)
	is_public = models.BooleanField(default=0)
	docInsideText = models.TextField(blank=True, null=True)

class tags(models.Model):
	name = models.CharField(max_length=250)
	is_delete = models.BooleanField(default=0)

class document_tag(models.Model):
	name = models.CharField(max_length=250)
	document_file = models.ForeignKey(document_file, on_delete=models.SET_NULL, null=True, blank=True)
	document_tag = models.ForeignKey(tags, on_delete=models.SET_NULL, null=True, blank=True)

class audit_trail(models.Model):
	document_file = models.ForeignKey(document_file, on_delete=models.SET_NULL, null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	updatesText = models.TextField(blank=True, null=True)
	update_date = models.DateTimeField(auto_now_add=True)