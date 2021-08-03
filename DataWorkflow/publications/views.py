from django.shortcuts import render, get_object_or_404, redirect
from .models import Publication, Creator
from .forms import PublicationForm, CreatorForm


# Create your views here.

def home(request):
    return render(request, 'publications/home.html')

def publication_list(request):

    publications = Publication.objects.all()

    return render(request, 'publications/publication_list.html', {'publications': publications})


def publication_detail(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    return render(request, 'publications/publication_detail.html', {'publication': publication})


def publication_new(request):
    if request.method == "POST":
        form = PublicationForm(request.POST)
        if form.is_valid():
            publication = form.save(commit=False)
            publication.save()
            return redirect('publication_detail', pk=publication.pk)
    else:
        form = PublicationForm()
    return render(request, 'publications/publication_edit.html', {'form': form})


def publication_edit(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    if request.method == "POST":
        form = PublicationForm(request.POST, instance=publication)
        if form.is_valid():
            publication = form.save(commit=False)
            publication.save()
            return redirect('publication_detail', pk=publication.pk)
    else:
        form = PublicationForm(instance=publication)
    return render(request, 'publications/publication_edit.html', {'form': form})


def creator_list(request):

    creators = Creator.objects.all()

    return render(request, 'publications/creator_list.html', {'creators': creators})


def creator_detail(request, pk):
    creator = get_object_or_404(Creator, pk=pk)
    return render(request, 'publications/creator_detail.html', {'creator': creator})


def creator_edit(request, pk):
    creator = get_object_or_404(Creator, pk=pk)
    if request.method == "POST":
        form = CreatorForm(request.POST, instance=creator)
        if form.is_valid():
            creator = form.save(commit=False)
            creator.save()
            return redirect('creator_detail', pk=creator.pk)
    else:
        form = CreatorForm(instance=creator)
    return render(request, 'publications/creator_edit.html', {'form': form})
