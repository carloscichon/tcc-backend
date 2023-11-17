from django.urls import path
from . import views

urlpatterns = [
    path('', views.rooms, name="rooms"),
    path('newroom/', views.new, name='newroom'),
    path('<slug:slug>/', views.room, name='room'),
    path('<slug:slug>/leave/', views.leave, name='leave'),
    path('<slug:slug>/sendFrame/', views.image, name='image'),
    path('<slug:slug>/start/', views.start, name='start'),
    path('<slug:slug>/avgExp/', views.getAvgExp, name='avgExp'),

]
