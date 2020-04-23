from django.urls import path
from . import views

urlpatterns = [
    path('', views.publication_list, name='publication_list'), ]