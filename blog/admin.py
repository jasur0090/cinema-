from django.contrib import admin
from .models import Category, Article

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'rating', 'views', 'created_at', 'publish']
    list_filter = ['category', 'publish', 'created_at']
    search_fields = ['title', 'content']
    list_editable = ['publish']
    readonly_fields = ['views', 'created_at', 'updated_at']