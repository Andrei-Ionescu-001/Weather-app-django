from django.urls import path
# from django.contrib.auth import views as auth_view
from . import views
# from django.contrib.auth import views as auth_views

app_name='cities'

urlpatterns = [
    path('', views.LocationList.as_view(), name="all"),
    path('new/', views.CreateCityView.as_view(), name='new'),
    path("<str:name>/<int:pk>/",views.LocationDetailView.as_view(),name="single"),
    path("delete/<str:name>/<int:pk>/", views.LocationDeleteView.as_view(), name="delete"),

]