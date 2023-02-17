from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from docs.models import document_type, document_file, tags, document_tag, audit_trail
from personnel.models import Department, Profile
from pdf2image import convert_from_path
import cv2, random, pytesseract, string, PyPDF2, uuid

def docsIndex(request):
	return render(request, 'upload_file.html')

@login_required(login_url='/accounts/login/')
def documentUpload(request):
	documentTypesList = document_type.objects.all()
	departments = Department.objects.filter(status="active", is_delete="0")
	if request.method == 'POST':
		if request.POST['DocumentType'] == "others":
			DocumentTypeDetails = document_type.objects.filter(name=request.POST['DocumentNewType'])
			if len(DocumentTypeDetails) != 0:
				documentTypes = DocumentTypeDetails[0].pk
			else:
				NewDocumentType = document_type()
				NewDocumentType.name = request.POST['DocumentNewType']
				NewDocumentType.save()
				documentTypes = NewDocumentType.pk
		else:
			documentTypes = request.POST['DocumentType']

		departmentsDetails = Department.objects.get(pk=request.POST['DocumentOwner'])
		documentType = document_type.objects.get(pk=documentTypes)
		DocumentNameStrip = request.POST['DocumentName'].strip()
		newDocumentFile = document_file()
		newDocumentFile.name = DocumentNameStrip
		newDocumentFile.description = request.POST['DocumentDescription']
		newDocumentFile.docType = documentType
		newDocumentFile.docOwner = departmentsDetails
		newDocumentFile.documentController = request.POST['DocumentController']
		is_public = request.POST.get('IsPublic', False) #on or false :)
		if is_public != False:
			newDocumentFile.is_public = 1
		else:
			newDocumentFile.is_public = 0

		uploaded_file = request.FILES.get('upload_file', False)
		if uploaded_file != False:
			uploaded_file = request.FILES['upload_file']
			fs = FileSystemStorage()
			filenameExt = uploaded_file.name.split(".")
			filename = get_random_string(164)+"."+filenameExt[1]
			newDocumentFile.filePath = filename
			fs.save(filename, uploaded_file)
			if filenameExt[1] == "pdf":
				# creating a pdf file object
				pdfFileObj = open(settings.MEDIA_ROOT+filename, 'rb')
				# creating a pdf reader object
				pdfReader = PyPDF2.PdfReader(pdfFileObj,  strict=False)
				# printing number of pages in pdf file
				pdftextVal = ""
				number_of_pages = len(pdfReader.pages)
				if (number_of_pages > 1):
					for x in range(number_of_pages):
						pageObj = pdfReader.pages(x)
						pdftextVal += pageObj.extractText() + "</n>"

				if(len(pdftextVal) == 0):
					myuuid = uuid.uuid4()
					images = convert_from_path(settings.MEDIA_ROOT+filename, 500, output_file=str(myuuid), fmt='jpeg', output_folder=settings.MEDIA_ROOT)
					img = cv2.imread(settings.MEDIA_ROOT+str(myuuid)+"0001-1.jpg")
					text = pytesseract.image_to_string(img)
					newDocumentFile.docInsideText = text
				else:
					newDocumentFile.docInsideText = pdftextVal
			elif filenameExt[1] == "doc" or filenameExt[1] == "docx":
				print("document file here!")
			else:
				# if image file
				# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
				img = cv2.imread(settings.MEDIA_ROOT+filename)
				text = pytesseract.image_to_string(img)
				newDocumentFile.docInsideText = text

		newDocumentFile.save()
		tagAddList = request.POST.getlist('tags[]')
		if len(tagAddList) != 0:
			for tag in tagAddList:
				tagDetails = tags.objects.filter(name=tag)
				if len(tagDetails) != 0:	
					newDocumentTag = document_tag()
					newDocumentTag.document_file = newDocumentFile
					newDocumentTag.document_tag = tagDetails[0]
					newDocumentTag.save()
				else:
					newTag = tags()
					newTag.name = tag
					newTag.save()
					newDocumentTag = document_tag()
					newDocumentTag.document_file = newDocumentFile
					newDocumentTag.document_tag = newTag
					newDocumentTag.save()
		documentType = document_type.objects.get(pk=documentTypes)
		listOfTags = document_tag.objects.filter(document_file=newDocumentFile.pk)
		return render(request, 'upload_success.html', {"documentFileDetails": newDocumentFile, "tags": listOfTags})
	else:
		return render(request, 'upload.html', {"docTypeList": documentTypesList, "departments": departments})

def viewDocument(request, document_id):
	DocumentDetails = document_file.objects.get(pk=document_id)
	documentTypesList = document_type.objects.all().order_by("name")
	departments = Department.objects.filter(status="active", is_delete="0")
	listOfTags = document_tag.objects.filter(document_file=document_id)
	if DocumentDetails.filePath is None or DocumentDetails.filePath == "":
		DocumentDetails.documentextention = ""
	else:
		documentPathsplit = DocumentDetails.filePath.split(".")
		DocumentDetails.documentextention = documentPathsplit[1]
	return render(request, 'view_document.html', {"DocumentDetails":DocumentDetails, "docTypeList": documentTypesList, "departments": departments, "DocumentTags":listOfTags, "documentId": document_id})

def documentSearch(request):
	typesId = []
	tagsId = []
	documentFileList = []
	documentTypesList = document_type.objects.all()
	listOfTags = tags.objects.all()
	departments = Department.objects.filter(status="active", is_delete="0")
	documentOwner = 0
	if request.method == 'POST':
		documentOwner = request.POST.get('documentOwnerSelect', 0)
		typesList = request.POST.getlist('documenttypes[]')
		tagsList = request.POST.getlist('documenttags[]')
		if len(typesList) != 0:
			for types in typesList:
				typesId.append(int(types))
		if len(tagsList) != 0:
			for tag in tagsList:
				tagsId.append(int(tag))
		if documentOwner != "0":
			if len(typesList) != 0:
				if len(tagsList) != 0:
					filtedTagsList = document_tag.objects.filter(document_tag__in=tagsList)
					if len(filtedTagsList) != 0:
						for filteredTags in filtedTagsList:
							documentFileList.append(filteredTags.document_file.pk)
						if request.user.is_authenticated:
							listOfDocument = document_file.objects.filter(docOwner__pk=documentOwner, docType__pk__in=typesList, pk__in=documentFileList)
						else:
							listOfDocument = document_file.objects.filter(docOwner__pk=documentOwner, docType__pk__in=typesList, pk__in=documentFileList, is_public=1)
				else:
					if request.user.is_authenticated:
						listOfDocument = document_file.objects.filter(docOwner__pk=documentOwner, docType__pk__in=typesList)
					else:
						listOfDocument = document_file.objects.filter(docOwner__pk=documentOwner, docType__pk__in=typesList, is_public=1)
			elif len(tagsList) != 0:
				filtedTagsList = document_tag.objects.filter(document_tag__in=tagsList)
				if len(filtedTagsList) != 0:
					for filteredTags in filtedTagsList:
						documentFileList.append(filteredTags.document_file.pk)
				if request.user.is_authenticated:
					listOfDocument = document_file.objects.filter(docOwner__pk=documentOwner, pk__in=documentFileList)
				else:
					listOfDocument = document_file.objects.filter(docOwner__pk=documentOwner, pk__in=documentFileList, is_public=1)
			else:
				if request.user.is_authenticated:
					listOfDocument = document_file.objects.filter(docOwner__pk=documentOwner)
				else:
					listOfDocument = document_file.objects.filter(docOwner__pk=documentOwner, is_public=1)
		else:
			if len(typesList) != 0:
				if len(tagsList) != 0:
					filtedTagsList = document_tag.objects.filter(document_tag__in=tagsList)
					if len(filtedTagsList) != 0:
						for filteredTags in filtedTagsList:
							documentFileList.append(filteredTags.document_file.pk)
						if request.user.is_authenticated:
							listOfDocument = document_file.objects.filter(docType__pk__in=typesList, pk__in=documentFileList)
						else:
							listOfDocument = document_file.objects.filter(docType__pk__in=typesList, pk__in=documentFileList, is_public=1)
				else:
					if request.user.is_authenticated:
						listOfDocument = document_file.objects.filter(docType__pk__in=typesList)
					else:
						listOfDocument = document_file.objects.filter(docType__pk__in=typesList, is_public=1)
			elif len(tagsList) != 0:
				filtedTagsList = document_tag.objects.filter(document_tag__in=tagsList)
				if len(filtedTagsList) != 0:
					for filteredTags in filtedTagsList:
						documentFileList.append(filteredTags.document_file.pk)

				if request.user.is_authenticated:
					listOfDocument = document_file.objects.filter(pk__in=documentFileList)
				else:
					listOfDocument = document_file.objects.filter(pk__in=documentFileList, is_public=1)
			else:
				if request.user.is_authenticated:
					listOfDocument = document_file.objects.all()
				else:
					listOfDocument = document_file.objects.filter(is_public=1)
	else:
		if request.user.is_authenticated:
			listOfDocument = document_file.objects.all()
		else:
			listOfDocument = document_file.objects.filter(is_public=1)

	return render(request, 'search.html', {"documents": listOfDocument, "docTypeList": documentTypesList, "post_types":typesId, "post_tags":tagsId, "listOfTags":listOfTags, "departments": departments, "documentOwner":int(documentOwner)})

def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    # print random string
    return str(result_str)



def downloadFile(request, filename=''):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = '444.docx'
    # Define the full file path
    filepath = BASE_DIR + '/OCR/media/' + filename
    # Open the file for reading content
    path = open(filepath,  encoding="utf8")
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response


@login_required(login_url='/accounts/login/')
def editDocument(request, document_id):
	DocumentDetails = document_file.objects.get(pk=document_id)
	documentTypesList = document_type.objects.all().order_by("name")
	departments = Department.objects.filter(status="active", is_delete="0")
	listOfTags = document_tag.objects.filter(document_file=document_id)
	postvalue = 0
	if DocumentDetails.filePath is None or DocumentDetails.filePath == "":
		DocumentDetails.documentextention = ""
	else:
		documentPathsplit = DocumentDetails.filePath.split(".")
		DocumentDetails.documentextention = documentPathsplit[1]
	if request.method == 'POST':
		postvalue = 1
		DocumentDetails.name = request.POST['DocumentName'].strip()
		DocumentDetails.description = request.POST['DocumentDescription']
		DocumentDetails.documentController = request.POST['DocumentController']
		if request.POST['DocumentType'] == "others":
			DocumentTypeDetails = document_type.objects.filter(name=request.POST['DocumentNewType'])
			if len(DocumentTypeDetails) != 0:
				documentTypes = DocumentTypeDetails[0].pk
			else:
				NewDocumentType = document_type()
				NewDocumentType.name = request.POST['DocumentNewType']
				NewDocumentType.save()
				documentTypes = NewDocumentType.pk
		else:
			documentTypes = request.POST['DocumentType']
		documentType = document_type.objects.get(pk=documentTypes)
		DocumentDetails.docType = documentType
		departmentsDetails = Department.objects.get(pk=request.POST['DocumentOwner'])
		DocumentDetails.docOwner = departmentsDetails
		listOfTags = document_tag.objects.filter(document_file=document_id)
		listOfTags.delete()
		is_public = request.POST.get('IsPublic', False) #on or false :)
		if is_public != False:
			DocumentDetails.is_public = 1
		else:
			DocumentDetails.is_public = 0
		DocumentDetails.save()
		tagAddList = request.POST.getlist('tags[]')
		if len(tagAddList) != 0:
			for tag in tagAddList:
				tagDetails = tags.objects.filter(name=tag)
				if len(tagDetails) != 0:	
					newDocumentTag = document_tag()
					newDocumentTag.document_file = DocumentDetails
					newDocumentTag.document_tag = tagDetails[0]
					newDocumentTag.save()
				else:
					newTag = tags()
					newTag.name = tag
					newTag.save()
					newDocumentTag = document_tag()
					newDocumentTag.document_file = DocumentDetails
					newDocumentTag.document_tag = newTag
					newDocumentTag.save()
		uploaded_file = request.FILES.get('upload_file', False)
		if uploaded_file != False:
			uploaded_file = request.FILES['upload_file']
			fs = FileSystemStorage()
			filenameExt = uploaded_file.name.split(".")
			oldfilePath = DocumentDetails.filePath
			oldFilePathSplit = oldfilePath.split(".")
			filename = get_random_string(164)+"."+filenameExt[1]
			DocumentDetails.filePath = filename
			fs.save(filename, uploaded_file)

			if filenameExt[1] == "pdf":
				# creating a pdf file object
				pdfFileObj = open(settings.MEDIA_ROOT+filename, 'rb')
				# creating a pdf reader object
				pdfReader = PyPDF2.PdfReader(pdfFileObj,  strict=False)
				# printing number of pages in pdf file
				pdftextVal = ""
				number_of_pages = len(pdfReader.pages)
				if (number_of_pages > 1):
					for x in range(number_of_pages):
						pageObj = pdfReader.pages(x)
						pdftextVal += pageObj.extractText() + "</n>"

				if(len(pdftextVal) == 0):
					myuuid = uuid.uuid4()
					images = convert_from_path(settings.MEDIA_ROOT+filename, 500, output_file=str(myuuid), fmt='jpeg', output_folder=settings.MEDIA_ROOT)
					# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
					img = cv2.imread(settings.MEDIA_ROOT+str(myuuid)+"0001-1.jpg")
					text = pytesseract.image_to_string(img)
					DocumentDetails.docInsideText = text
					DocumentDetails.save()
				else:
					DocumentDetails.docInsideText = pdftextVal
					DocumentDetails.save()
			elif filenameExt[1] == "doc" or filenameExt[1] == "docx":
				print("document file here!")
			else:
				# if image file
				# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
				img = cv2.imread(settings.MEDIA_ROOT+filename)
				text = pytesseract.image_to_string(img)
				DocumentDetails.docInsideText = text
				DocumentDetails.save()
		# trail
		current_user =  request.user
		newTrail = audit_trail()
		newTrail.user = current_user.id
		newTrail.document_file = DocumentDetails
		newTrail.updatesText = "sample"
		newTrail.save()

		listOfTags = document_tag.objects.filter(document_file=document_id)
	return render(request, 'edit_document.html', {"DocumentDetails":DocumentDetails, "docTypeList": documentTypesList, "departments": departments, "DocumentTags":listOfTags, "documentId": document_id, "updated": postvalue})

def updateDocument(request, document_id):
	listOfDocument = document_file.objects.all()
	return render(request, 'search.html', {"documents": listOfDocument})
