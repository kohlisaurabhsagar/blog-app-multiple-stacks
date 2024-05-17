from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm
# from django.contrib import messages
from django.contrib.auth.decorators import login_required

def SignUp(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users-login')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'sign_up.html', context)

@login_required
def profile(request):
    return render(request, 'profile.html')


