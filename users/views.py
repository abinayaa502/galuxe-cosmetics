from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User

@login_required
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})

def profile_redirect(request):
    return redirect('profile')
