from django.shortcuts import render
from .models import Publication


# Create your views here.

def publication_list(request):

    publications = Publication.objects.all()


    return render(request, 'publications/publication_list.html', {'publications': publications})

