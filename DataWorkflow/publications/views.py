from django.shortcuts import render

# Create your views here.

def publication_list(request):
    return render(request, 'publications/publication_list.html', {})