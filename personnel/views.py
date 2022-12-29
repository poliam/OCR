from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse
from personnel.models import Department, Profile
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url='/accounts/login/')
def personelIndex(request):
	try:
		listDepartment = Department.objects.all().order_by('status')
	except:
		listDepartment = []

	try:
		listPersonnel = Profile.objects.filter(status="active")
	except:
		listPersonnel = []

	return render(request, 'personnel_dashboard.html', {"listDept": listDepartment, "listPersonnel": listPersonnel})

@login_required(login_url='/accounts/login/')
def createDepartment(request):
	data = {}
	newDepartment = Department()
	newDepartment.departmentName = request.POST['DepartmentName']
	newDepartment.save()
	data['success'] = 1
	return JsonResponse(data, safe=False)

@login_required(login_url='/accounts/login/')
def getDepartmentByName(request):
	data = {}
	request.GET['deptId']
	if 'editDepartmentId' not in request.GET:
	   deptId = 0
	else:
	   deptId = request.POST['deptId']
	try:
		department = Department.objects.get(departmentName=request.GET['DepartmentName'])
		print(deptId+"=="+department.pk)
		if deptId == department.pk:
			data['status'] = "available"
		else:	
			data['status'] = "not available"
			data["errormsg"] = "There is already a department with that name!"
	except:
		data['status'] = "available"

	return JsonResponse(data, safe=False)

@login_required(login_url='/accounts/login')
def getDepartmentById(request):
	data = {}
	try:
		departmentDetails = Department.objects.get(pk=request.GET['DeptId'])
		data['status'] = "success"
		data['departmentName'] = departmentDetails.departmentName
		data['departmentStatus'] = departmentDetails.status
		data['departmentId'] = departmentDetails.pk
	except:
		data['status'] = "failed"
		data['errormsg'] = "department does not exist"

	return JsonResponse(data, safe=False)

@login_required(login_url='/accounts/login/')
def checkPersonnel(request):
	data = {}
	username = request.POST['Username']
	try:
		User.objects.get(username=username)
		data["status"] = "failed"
		data["errormsg"] = "user already exists!"
		return JsonResponse(data, safe=False)
	except:
		data["status"] = "available"

	firstNameForm = request.POST['FirstName']
	lastnameForm = request.POST['LastName']

	try:
		userProfileDetails = Profile.objects.get(firstName=firstNameForm, lastName=lastnameForm);
		data['status'] = "failed"
		data["errormsg"] = "user already exists!"
	except:
		data['status'] = "available"
		
	return JsonResponse(data, safe=False)

@login_required(login_url='/accounts/login/')
def createPersonnel(request):
	data = {}
	username = request.POST['Username']
	firstNameForm = request.POST['FirstName']
	middleNameForm = request.POST['MiddleName']
	lastnameForm = request.POST['LastName']
	emailForm = request.POST['Email']
	contactNumberForm = request.POST['ContactNumber']
	passwordForm = request.POST['Password']
	departmentForm = request.POST['Department']
	departmentDetails = Department.objects.get(pk=departmentForm)
	try:
		user = User.objects.create_user(username=username, email=emailForm, password=passwordForm, first_name=firstNameForm, last_name=lastnameForm)
		data['status'] = "success"
		newProfile = Profile()
		newProfile.firstName = firstNameForm
		newProfile.middleName = middleNameForm
		newProfile.lastName = lastnameForm
		newProfile.email = emailForm
		newProfile.contactNumber = contactNumberForm
		newProfile.department = departmentDetails
		newProfile.userId = user
		newProfile.save()
		data['status'] = "success"
	except:
		data['status'] = "failed"
		data['errormsg'] = "Error on creating a user"

	return JsonResponse(data, safe=False)

@login_required(login_url='/accounts/login/')
def updateDepartment(request):
	data = {}
	departmentId = request.POST.get('editDepartmentId', False)
	try:
		departmentDetails = Department.objects.get(pk=departmentId)
		try:
			department = Department.objects.get(departmentName=request.POST['EditDepartmentName'])
			if department.pk == departmentDetails.pk:
				departmentDetails.departmentName = request.POST['EditDepartmentName']
				departmentDetails.status = request.POST['EditDepartmentStatus']
				departmentDetails.save()
				data['status'] = "success"
			else:
				data['status'] = "failed"
				data['errormsg'] = "That department already exists!"
		except:
			departmentDetails.departmentName = request.POST['EditDepartmentName']
			departmentDetails.status = request.POST['EditDepartmentStatus']
			departmentDetails.save()
			data['status'] = "success"
	except:
		data['status'] = "failed"
		data['errormsg'] = "department does not exist"

	return JsonResponse(data, safe=False)
