from django.urls import path
from . import views

urlpatterns = [
    path('', views.publication_list, name='publication_list'),
    path('publication/<int:pk>/', views.publication_detail, name='publication_detail'),
]