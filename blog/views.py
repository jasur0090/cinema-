from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User


def index(request):
    # Avtomatik kirish - agar hech qanday foydalanuvchi kirmagan bo'lsa va superuser mavjud bo'lsa
    if not request.user.is_authenticated:
        # Birinchi superuser hisobini olish
        superuser = User.objects.filter(is_superuser=True).first()
        if superuser:
            # Avtomatik kirish
            user = authenticate(username=superuser.username, password=None, force_login=True)
            if user:
                login(request, user)

    categories = Category.objects.all()
    articles = Article.objects.filter(publish=True)
    sort_field = request.GET.get('sort')

    if sort_field:
        articles = articles.order_by(sort_field)
    else:
        articles = articles.order_by('-created_at')

    paginator = Paginator(articles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Cinema World - Home',
        'categories': categories,
        'page_obj': page_obj,
        'articles': articles
    }
    return render(request, 'blog/index.html', context)


def category_page(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, pk=category_id)
    articles = Article.objects.filter(category_id=category_id, publish=True)

    paginator = Paginator(articles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': f"{category.title} - Cinema World",
        'categories': categories,
        'page_obj': page_obj,
        'category': category
    }
    return render(request, 'blog/index.html', context)


def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    article.views += 1
    article.save()

    related_articles = Article.objects.filter(
        category=article.category, publish=True
    ).exclude(id=article.id)[:6]

    context = {
        'article': article,
        'title': f"{article.title} - Cinema World",
        'related_articles': related_articles
    }
    return render(request, 'blog/article_detail.html', context)


def add_article(request):
    # Avtomatik kirish - agar hech qanday foydalanuvchi kirmagan bo'lsa va superuser mavjud bo'lsa
    if not request.user.is_authenticated:
        # Birinchi superuser hisobini olish
        superuser = User.objects.filter(is_superuser=True).first()
        if superuser:
            # Avtomatik kirish
            user = authenticate(username=superuser.username, password=None, force_login=True)
            if user:
                login(request, user)

    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            messages.success(request, 'Movie added successfully!')
            return redirect('article', article.pk)
    else:
        form = ArticleForm()

    context = {
        'form': form,
        'title': 'Add Movie - Cinema World'
    }
    return render(request, 'blog/add_article.html', context)


def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Welcome back!')
                return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    context = {
        'login_form': form,
        'title': 'Login - Cinema World'
    }
    return render(request, 'blog/user_login.html', context)


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')



def register(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()  # foydalanuvchini saqlaymiz
            login(request, user)  # avtomatik login qilamiz
            messages.success(request, 'Welcome! You are now logged in.')
            return redirect('index')  # home sahifaga yo'naltiramiz
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()

    context = {
        'register_form': form,
        'title': 'Register - Cinema World'
    }
    return render(request, 'blog/register.html', context)


def search_results(request):
    word = request.GET.get('q')
    articles = Article.objects.filter(
        Q(title__icontains=word) | Q(content__icontains=word),
        publish=True
    )

    paginator = Paginator(articles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': word,
        'title': f'Search: {word} - Cinema World'
    }
    return render(request, 'blog/search_results.html', context)


def update_article(request, id):
    # Avtomatik kirish - agar hech qanday foydalanuvchi kirmagan bo'lsa va superuser mavjud bo'lsa
    if not request.user.is_authenticated:
        # Birinchi superuser hisobini olish
        superuser = User.objects.filter(is_superuser=True).first()
        if superuser:
            # Avtomatik kirish
            user = authenticate(username=superuser.username, password=None, force_login=True)
            if user:
                login(request, user)

    instance = get_object_or_404(Article, id=id)

    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movie updated successfully!')
            return redirect('article', id)
    else:
        form = ArticleForm(instance=instance)

    context = {
        'title': 'Update Movie - Cinema World',
        'form': form,
        'article': instance
    }
    return render(request, 'blog/add_article.html', context)


def delete_article(request, id):
    # Avtomatik kirish - agar hech qanday foydalanuvchi kirmagan bo'lsa va superuser mavjud bo'lsa
    if not request.user.is_authenticated:
        # Birinchi superuser hisobini olish
        superuser = User.objects.filter(is_superuser=True).first()
        if superuser:
            # Avtomatik kirish
            user = authenticate(username=superuser.username, password=None, force_login=True)
            if user:
                login(request, user)

    article = get_object_or_404(Article, id=id)

    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Movie deleted successfully!')
        return redirect('index')

    context = {
        'article': article,
        'title': 'Delete Movie - Cinema World'
    }
    return render(request, 'blog/confirm_delete.html', context)