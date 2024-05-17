from django.urls import path
from . import views  
from django.conf import settings  
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index-home'),
    path('post_details/<int:pk>', views.post_details, name='post-details'),
    path('post_edit/<int:pk>', views.post_edit, name='post-edit'),
    path('post_delete/<int:pk>', views.post_delete, name='post-delete'),
]

# Add this only if DEBUG is True, for serving media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

