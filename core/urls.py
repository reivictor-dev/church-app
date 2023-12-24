from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from ibbnj_church import settings
from .views import home, contato, user_login_view, register, about, posts

urlpatterns = [
    path('', home, name='home'),
    path('contato/', contato, name='contato'),
    path('login/', user_login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('about/', about, name='about'),
    path('posts/', posts, name='posts')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
