from django.urls import path
from . views import RegisterView, LogoutView, UserDetailView, ObtainTokenPairView, CustomTokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', ObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('userprofile/', UserDetailView.as_view(), name='user_detail'),
]
