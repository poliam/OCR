from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.conf import settings
# from pdf2image import convert_from_path
# import PyPDF2
import cv2
import pytesseract
# import uuid

def OCRIndex(request):
	return render(request, 'Homepage.html')

def trialPDF(request):
	# creating a pdf file object
	# pdfFileObj = open('C:/Users/polia/Bitnami Django Stack projects/OCR/OCR/media/sample.pdf', 'rb')
	# # creating a pdf reader object
	# pdfReader = PyPDF2.PdfFileReader(pdfFileObj,  strict=False)
	# # printing number of pages in pdf file
	# print(pdfReader.numPages)
	
	# returnVal = ""
	# if (pdfReader.numPages > 1):
	# 	for x in range(pdfReader.numPages):
	# 		pageObj = pdfReader.getPage(x)
	# 		returnVal += pageObj.extractText() + "</n>"

	# else:
	# 	# creating a page object
	# 	pageObj = pdfReader.getPage(0)
	
	# 	# extracting text from page
	# 	returnVal = pageObj.extractText()

	# if(len(returnVal) == 0):
	# 	myuuid = uuid.uuid4()
	# 	images = convert_from_path('C:/Users/polia/Bitnami Django Stack projects/OCR/OCR/media/sample.pdf', 500, poppler_path=r'C:\Program Files\poppler-22.04.0\Library\bin', output_file=str(myuuid), fmt='jpeg', output_folder='C:/Users/polia/Bitnami Django Stack projects/OCR/OCR/media/')
		
	# 	pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
	# 	print(images)
	# 	img = cv2.imread("C:\\Users\\polia\\Bitnami Django Stack projects\\OCR\\OCR\\media\\"+str(myuuid)+"0001-1.jpg")
	# 	text = pytesseract.image_to_string(img)
	# 	print(text)
	# # closing the pdf file object
	# pdfFileObj.close()
	
	return render(request, 'Homepage.html')
	

def trialImage(request):
	pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
	print(settings.MEDIA_ROOT)
	img = cv2.imread(settings.MEDIA_ROOT+"sample_image.jpg")
	# print(img)
	text = pytesseract.image_to_string(img)
	print(text)
	return render(request, 'Homepage.html')

	