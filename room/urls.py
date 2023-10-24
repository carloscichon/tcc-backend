from django.urls import path
from . import views

urlpatterns = [
    path('', views.rooms, name="rooms"),
    path('newroom/', views.new, name='newroom'),
    path('<slug:slug>/', views.room, name='room'),
    path('<slug:slug>/leave/', views.leave, name='leave'),
    path('<slug:slug>/sendFrame/', views.image, name='image'),
]
