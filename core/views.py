from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordChangeView
from .forms import LoginForm
from django.contrib import messages

from .models import Posts
from .forms import PostsModelForm, RegisterForm, UpdateUserForm, ContactForm


def home(request):
    return render(request, 'home.html')


def error_view(request, message):
    return render(request, 'error.html', {'message': message})


def contato(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             'Contato enviado com sucesso! Nossa equipe entrará em contato em breve.')
        else:
            messages.error(request, 'Verifique os campos')
            return render(request, 'contato.html', {'form': form})

    form = ContactForm()

    return render(request, 'contato.html', {'form': form})


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

# POST VIEW#


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


def update_post(request, id):
    post = get_object_or_404(Posts, id=id)

    if post.user_post != request.user:
        error_message = 'Você não tem permissão para editar este post.'
        return error_view(request, message=error_message)

    if request.method == 'POST':
        if request.user.is_authenticated and post.get_username == request.user.username:
            form = PostsModelForm(request.POST, request.FILES, instance=post)

            if form.is_valid():
                post.user_post = request.user
                form.save()

            return redirect('posts')
    else:
        form = PostsModelForm(instance=post)

    return render(request, "posts/update_post.html",  {'form': form, 'post': post})


def delete_post(request, id):

    post = get_object_or_404(Posts, id=id)

    if request.user.is_authenticated and post.get_username == request.user.username:
        if (request.method == "POST"):
            post.delete()
            return redirect("posts")
        else:
            return render(request, "posts/delete_post.html", {'post': post})
    else:
        error_message = 'Você não tem permissão para excluir este post.'
        return error_view(request, message=error_message)


# Password change view


class ChangePasswordView(PasswordChangeView):
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('perfil')
