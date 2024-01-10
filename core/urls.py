from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from ibbnj_church import settings
from .views import home, contato, user_login_view, register, about, posts, create_post, perfil, update_perfil, ChangePasswordView

urlpatterns = [
    path('', home, name='home'),
    path('contato/', contato, name='contato'),
    path('login/', user_login_view, name='login'),
    path('register/', register, name='register'),
    path('perfil/', perfil, name='perfil'),
    path('update_perfil/', update_perfil, name='update_perfil'),
    path('update_password/', ChangePasswordView.as_view(), name='update_password'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('about/', about, name='about'),
    path('posts/', posts, name='posts'),
    path('create_post/', create_post, name='create_post')
]
