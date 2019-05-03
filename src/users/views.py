from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from posts.models import Author, AuthorView, Post
from .forms import UserUpdateForm, ProfileUpdateForm, ValidAuthor, ValidUser

from chat.models import ChatRoom
from django.contrib.auth.models import User

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
    authorV = Author.objects.get(id=id)
    publicaciones = Post.objects.filter(author = author)
    numero_publicaiones = publicaciones.count()

    if request.user.is_authenticated:
        AuthorView.objects.get_or_create(user=request.user, author=author)

###################################################
    user_list = author.user ## podemos filtrar aqui los ususarios
    if request.POST:
        sender = request.user
        receiver = request.POST.get("user")
        user_receiver = User.objects.filter(username=receiver)
        if sender.username != user_receiver[0].username:
            chat_rooms_1 = ChatRoom.objects.filter(
                sender=sender, receiver=user_receiver[0]
            )
            chat_rooms_2 = ChatRoom.objects.filter(
                sender=user_receiver[0], receiver=sender
            )
            if len(user_receiver) != 0:
                if len(chat_rooms_1) == 0 and len(chat_rooms_2) == 0:
                    chat_room = ChatRoom.objects.create(
                        sender=sender, receiver=user_receiver[0]
                    )
                    chat_room.save()  #aqui se guarda el grupo del chat
                    id_chat = str(chat_room.id)
                    return redirect("/chat/"+id_chat) ## te redirecciona al chat list
                else:
                    return render(
                        request,
                        "users/author_details.html",
                        {
                            'author': author,
                            'authorV': authorV,
                            'publicaciones': publicaciones,
                            'numero_publicaciones': numero_publicaiones,
                            "user_filtered": user_list,
                            "no_user": "Chat already exists",
                        },
                    )
            else:
                return render(
                    request,
                    "users/author_details.html",
                    {       'author': author,
        'authorV': authorV,
        'publicaciones' : publicaciones,
        'numero_publicaciones' : numero_publicaiones,
                            "user_filtered": user_list, "no_user": "No such user"},
                )
        else:
            return render(
                request,
                "users/author_details.html",
                {
                    'author': author,
                    'authorV': authorV,
                    'publicaciones': publicaciones,
                    'numero_publicaciones': numero_publicaiones,
                    "user_filtered": user_list,
                    "no_user": "Same user is not allowed.",
                },
            )
    else:
        return render(
            request, "users/author_details.html", {
                'author': author,
                'authorV': authorV,
                'publicaciones': publicaciones,
                'numero_publicaciones': numero_publicaiones,
                                    "user_filtered": user_list,
                                    "no_user": ""
                                    }
        )
############################################


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
            messages.success(request, f'¡Tu cuenta ha sido actualizada!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.author)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)