from django.shortcuts import render

def tryon_index(request):
    return render(request, 'virtual_tryon/index.html')
