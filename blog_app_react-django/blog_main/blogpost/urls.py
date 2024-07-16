from django.urls import path
from . import views  
from django.conf import settings  
from django.conf.urls.static import static


urlpatterns = [
    path('', views.PostModelListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>', views.PostModelDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/comments', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('posts/<int:post_id>/comments/<int:pk>', views.CommentsDetailView.as_view(), name='comment-list-update-delete')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

