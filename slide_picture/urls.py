from django.urls import path
from . import views

urlpatterns = [
    path('', views.PictureListView.as_view(), name='picture')
]
