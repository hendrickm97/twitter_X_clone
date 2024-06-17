from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Tweet
from .forms import TweetForm, SingUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms

def home(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, "Seu tweet foi postado com sucesso!")
                return redirect('home')

        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"tweets": tweets, "form":form})

    else:
        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"tweets": tweets})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.success(request, "Você Precisa estar logado!")
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        tweets = Tweet.objects.filter(user_id=pk).order_by("-created_at")

        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)

            current_user_profile.save()

        return render(request, 'profile.html', {"profile": profile, "tweets": tweets})

    else:
        messages.success(request, "Você Precisa estar logado!")
        return redirect('home')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Você entrou na sua conta!"))
            return redirect('home')
        else:
            messages.success(request, ("Ocorreu um erro, por favor tente novamente!"))
            return redirect('login')
    else:
        return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, ("Você saiu da sua conta!"))
    return redirect('home')


def register(request):
    form = SingUpForm()
    if request.method == "POST":
        form = SingUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Você se cadastrou com sucesso!!!"))
            return redirect('home')

    return render(request, "register.html", {'form': form})


def tweet_like(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if tweet.likes.filter(id=request.user.id):
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("Você precisa estar logado para deixar um like!"))
        return redirect('home')


def delete_tweet(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if request.user.username == tweet.user.username:
            tweet.delete()
            messages.success(request, ("Tweet deletado com sucesso!"))
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.success(request, ("esse tweet não é seu!"))
            return redirect('home')

    else:
        messages.success(request, ("Por favor faça o login na sua conta..."))
        return redirect(request.META.get("HTTP_REFERER"))


def update_tweet(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if request.user.username == tweet.user.username:
           form = TweetForm(request.POST or None, instance=tweet)
           if request.method == "POST":
               if form.is_valid():
                   tweet = form.save(commit=False)
                   tweet.user = request.user
                   tweet.save()
                   messages.success(request, "Seu tweet foi editado com sucesso!")
                   return redirect('home')
           else:
             return render(request, "update_tweet.html", {"form": form, 'tweet': tweet})
        else:
            messages.success(request, ("esse tweet não é seu!"))
            return redirect('home')

    else:
        messages.success(request, ("Por favor faça o login na sua conta..."))
        return redirect('home')

