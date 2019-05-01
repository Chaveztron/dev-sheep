from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from posts.views import \
    (index, blog, post, search, \
    post_update, post_delete, post_create, search_by_type)
from users import views as user_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', user_views.profile, name='profile'),
    path('', index),
    path('blog/', blog, name='post-list'),
    path('search/', search, name='search'),
    path('search-type/<id>', search_by_type, name='search-type'),
    path('create/', post_create, name='post-create'),
    path('post/<id>/', post, name='post-detail'),
    path('post/<id>/update/', post_update, name='post-update'),
    path('post/<id>/delete/', post_delete, name='post-delete'),
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),

    path('validar/', user_views.validar_author, name='valid'),
    path('author/<id>/', user_views.author_detalles, name='detalles_usuario')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
