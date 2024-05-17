from django.urls import path
from .import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('sign-up/',views.SignUp, name='users-sign-up'),
     path('profile/',views.profile, name='users-profile'),
    path('login/',auth_view.LoginView.as_view(template_name='login.html'), name='users-login'),
    path('logout/',auth_view.LogoutView.as_view(template_name='logout.html'), name='users-logout'),
]
