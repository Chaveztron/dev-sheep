from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserUpdateForm, ProfileUpdateForm, ValidAuthor


def validar_author(request):
    if request.method == 'POST':

        form = ValidAuthor(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, f'Ahora eres un author!')
            return redirect('profile')

    else:
        form = ValidAuthor(instance=request.user)

    context = {
        'form':form,
    }

    return render(request, 'users/validar.html', context)




@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form: ProfileUpdateForm = ProfileUpdateForm(request.POST,
                                                      request.FILES,
                                                      instance=request.user.author)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.author)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)