from django.urls import path
from . import views

urlpatterns = [
    path('', views.publication_list, name='publication_list'),
    path('publication/<int:pk>/', views.publication_detail, name='publication_detail'),
    path('publication/new/', views.publication_new, name='publication_new'),
    path('publication/<int:pk>/edit/', views.publication_edit, name='publication_edit'),
]