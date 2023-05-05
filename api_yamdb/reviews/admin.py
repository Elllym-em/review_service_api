from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    )
    search_fields = ('username', 'email',)
    list_filter = ('email',)
    empty_value_display = '-пусто-'


admin.site.register(User)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('slug',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Category)


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('slug',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Genre)


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'category',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Title)


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'pub_date',
        'title',
        'score',
        'text',
    )
    search_fields = ('author', 'title',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Review)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'pub_date',
        'review',
        'text',
    )
    search_fields = ('author', 'review',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Comment)
