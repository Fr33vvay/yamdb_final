from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Администрирование категорий.
    """
    list_display = ('id', 'name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Администрирование жанров.
    """
    list_display = ('id', 'name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """
    Администрирование произведений.
    """
    list_display = ('id', 'name', 'year', 'description', 'category')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    """
    Администрирование комментариев к отзывам.
    """
    list_display = ('text', 'pub_date', 'author',)
    search_fields = ('author',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    """
    Администрирование отзывов.
    """
    list_display = ('text', 'pub_date', 'author',)
    search_fields = ('author',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
