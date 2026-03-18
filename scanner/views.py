from django.shortcuts import render

def scanner_index(request):
    return render(request, 'scanner/index.html')
