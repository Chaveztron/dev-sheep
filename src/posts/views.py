from django.contrib import messages
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import CommentForm, PostForm
from .models import Post, Author, PostView


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def search(request):
    #esto es lo de la pagina principal
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    #Query SET
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()

    post_list = queryset
    #QUERY de busquedas
    paginator = Paginator(post_list, 6)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    #asta aqui termina
    #paginacion
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    #paginacion
    context = {
        #otros contextos
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'category_count': category_count
        #otros
    }
    return render(request, 'search_results.html', context)

##########################################

def search_by_type(request, id):
    #esto es lo de la pagina principal
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    post_list = Post.objects.filter(categories=id)[0:]
    paginator = Paginator(post_list, 6)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    #asta aqui termina
    #paginacion
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    #paginacion
    context = {
        #otros contextos
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'category_count': category_count
        #otros
    }
    return render(request, 'search_results.html', context)


#############################################


def get_category_count():
    queryset = Post.objects.values('categories__title', 'categories__id').annotate(Count('categories__title'))
    return queryset


def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    context = {
        'object_list': featured,
        'latest': latest
    }
    return render(request, 'index.html', context)


def blog(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    post_list = Post.objects.order_by('-timestamp')[0:]
    paginator = Paginator(post_list, 6)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'category_count': category_count

    }
    return render(request, 'blog.html', context)


def post(request, id):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    post = get_object_or_404(Post, id=id)
    authors = Author.objects.all()

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': post.pk
            }))
    context = {
        'form': form,
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count,
        'authors':authors
    }

    return render(request, 'post.html', context)


def post_create(request):
    title = 'Crea'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            messages.success(request, f'¡Tu oferta ha sido publicada!')
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)


def post_update(request, id):
    title = 'Modifica'
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    author = get_author(request.user)
    if post.author.user == request.user:
        if request.method == "POST":
            if form.is_valid():
                form.instance.author = author
                form.save()
                messages.success(request, f'¡Tu oferta ha sido actualizada!')
                return redirect(reverse("post-detail", kwargs={
                    'id': form.instance.id
                }))
        context = {
            'title': title,
            'form': form
        }
        return render(request, "post_create.html", context)
    else:
        return post_create(request)


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author.user == request.user:
        post.delete()
        messages.success(request, f'¡Tu oferta ha sido borrada!')
        return redirect(reverse("post-list"))
    else:
        return post_create(request)