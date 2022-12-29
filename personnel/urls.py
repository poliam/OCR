from django.urls import path

from . import views

urlpatterns = [
    path('', views.personelIndex, name='personnelIndex'),
    path('create_department', views.createDepartment, name='createDepartment'),
    path('get_department_Name', views.getDepartmentByName, name='getDepartmentByName'),
    path('get_department_Id', views.getDepartmentById, name='getDepartmentById'),
    path('update_department', views.updateDepartment, name='updateDepartment'),
    path('check_personnel', views.checkPersonnel, name='checkPersonnel'),
    path('create_personnel', views.createPersonnel, name='createPersonnel'),
    path('get_personnel_id', views.getPersonnelById, name='getPersonnelById'),
]