from django.db import models

# Create your models here.
class Document_file(models.Model):
	document_name = models.CharField(max_length=250)
	document_details = models.CharField(max_length=250, default="active")
	models.FileField(upload_to='media/', null=True)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now_add=True)
	is_delete = models.BooleanField(default=0)