from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .models import Posts
from .forms import PostsModelForm


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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


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
