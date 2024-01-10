from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordChangeView
from .forms import LoginForm
from django.contrib import messages

from .models import Posts
from .forms import PostsModelForm, RegisterForm, UpdateUserForm


def home(request):
    return render(request, 'home.html')


def contato(request):
    return render(request, 'contato.html')


def user_login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.error(request, "Invalid Username or Password")

            if user is not None:
                login(request, user)
                return redirect('/')
        else:
            return render(request, 'registration/login.html', {'form': form})
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def perfil(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        return redirect('login')

    return render(request, 'perfil.html', {'user': user})


def update_perfil(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST, instance=request.user)

            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Seu perfil foi atualizado')
                return redirect('perfil')
        else:
            user_form = UpdateUserForm(instance=request.user)

    return render(request, 'registration/update.html', {'user_form': user_form})


def about(request):
    return render(request, 'about.html')


def create_post(request):
    if request.user.is_authenticated:
        if str(request.method) == 'POST':
            form = PostsModelForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user_post = request.user
                post.save()

                messages.success(request, 'Postagem realizada com sucesso!')
                form = PostsModelForm()
            else:
                messages.error(
                    request, 'Erro ao tentar realizar postagem, tente novamente!')
        else:
            form = PostsModelForm()
        context = {
            'form': form
        }
        return render(request, 'posts/create_posts.html', context)
    else:
        return redirect('login')


def posts(request):
    context = {
        'posts': Posts.objects.all()
    }
    return render(request, 'posts/posts.html', context)


# Password change view
class ChangePasswordView(PasswordChangeView):
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('perfil')
