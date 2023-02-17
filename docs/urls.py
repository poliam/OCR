from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.docsIndex, name='docsIndex'),
    path('upload', views.documentUpload, name='documentUpload'),
    path('download/', views.downloadFile, name="downloadFile"),
    path('search/', views.documentSearch, name='documentSearch'),
    path('view_document/<int:document_id>', views.viewDocument, name='viewDocument'),
    path('edit_document/<int:document_id>', views.editDocument, name='editDocument'),
    path('update_documet/<int:document_id>', views.updateDocument, name='updateDocument'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)