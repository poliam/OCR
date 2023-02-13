"""OCR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views as OCRViews
from django.conf import settings
from django.conf.urls.static import static

app_name = "OCR"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", OCRViews.OCRIndex, name="OCRIndex"),
    path("trialPDF/", OCRViews.trialPDF, name="trialPDF"),
    path("trialImage/", OCRViews.trialImage, name="trialImage"),
    path("accounts/", include("django.contrib.auth.urls")),  # new
    path('personnel/', include('personnel.urls')),
    path('documents/', include('docs.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

