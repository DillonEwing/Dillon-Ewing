from django.contrib import admin

# Register your models here.
from blog.models import Category, Comment, Post


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_on', 'last_modified')
    list_filter = ('categories', 'created_on', 'author')
    search_fields = ('title', 'body')
    raw_id_fields = ('author',)
    filter_horizontal = ('categories',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_on')
    list_filter = ('created_on', 'post')
    search_fields = ('author', 'body')
    raw_id_fields = ('post',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)