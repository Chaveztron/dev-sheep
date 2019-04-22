from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from posts.models import Author, AuthorView
from .forms import UserUpdateForm, ProfileUpdateForm, ValidAuthor, ValidUser


@login_required
def validar_author(request):
    if request.method == 'POST':
        form_user = ValidUser(request.POST, instance=request.user)
        print(form_user)
        form = ValidAuthor(request.POST)
        if form.is_valid() and form_user.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            form.save()
            form_user.save()
            messages.success(request, f'Ahora eres un author!')
            return redirect('profile')

    else:
        form_user = UserUpdateForm(instance=request.user)
        form = ValidAuthor(instance=request.user)

    context = {
        'form':form,
        'form_user': form_user,
    }

    return render(request, 'users/validar.html', context)


def author_detalles(request, id):
    author = get_object_or_404(Author, id=id)

    if request.user.is_authenticated:
        AuthorView.objects.get_or_create(user=request.user, author=author)

    context = {
        'author': author,
    }

    return render(request, 'users/author_details.html', context)


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