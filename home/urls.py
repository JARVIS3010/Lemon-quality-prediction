from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path("", views.home, name="home"),
    path("prediction/", views.prediction, name="prediction"),
    path("predict/", views.prediction, name="predict"),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
]
