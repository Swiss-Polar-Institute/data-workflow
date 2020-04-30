from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('publications', views.publication_list, name='publication_list'),
    path('publication/<int:pk>/', views.publication_detail, name='publication_detail'),
    path('publication/new/', views.publication_new, name='publication_new'),
    path('publication/<int:pk>/edit/', views.publication_edit, name='publication_edit'),
    path('creators', views.creator_list ,name='creator_list'),
    path('creator/<int:pk>/', views.creator_detail, name='creator_detail'),
    path('creator/<int:pk>/edit/', views.creator_edit, name='creator_edit'),

]