from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.files.storage import FileSystemStorage

def docsIndex(request):
	return render(request, 'upload_file.html')

def uploadDocs(request):
	if request.method == 'POST' and request.FILES['document']:
		myfile = request.FILES['document']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		print(uploaded_file_url);
	return render(request, 'upload_success.html')


	