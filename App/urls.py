
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.Home, name="index"),
    path('register/', views.Enroll),
    path('all/', views.ListAll),
    path('student/delete/<str:Id>/', views.Delete),
    path('student/print/<str:Id>/', views.Print),
    path('student/<str:Id>/', views.SendStData),
    path('student/update/<str:Id>/', views.UpdateData),
]
