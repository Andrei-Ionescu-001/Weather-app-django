from django.urls import path
from django.contrib.auth import views as auth_view
from . import views
from django.contrib.auth import views as auth_views

app_name='accounts'

urlpatterns = [
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('password/', views.PasswordsChange.as_view(), name='password')
]