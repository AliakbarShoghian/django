# image_viewer/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('images/', views.image_slideshow, name='image_slideshow'), 
    path('manipulate_image/<int:image_id>/', views.manipulate_image, name='manipulate_image'),
]
