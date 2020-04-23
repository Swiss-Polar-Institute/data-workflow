from django.shortcuts import render, get_object_or_404
from .models import Publication
from .forms import PublicationForm


# Create your views here.

def publication_list(request):

    publications = Publication.objects.all()

    return render(request, 'publications/publication_list.html', {'publications': publications})


def publication_detail(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    return render(request, 'publications/publication_detail.html', {'publication': publication})


def publication_new(request):
    form = PublicationForm()
    return render(request, 'publications/publication_edit.html', {'form': form})

