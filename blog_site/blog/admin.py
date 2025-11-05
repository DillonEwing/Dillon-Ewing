"""ADMIN USE CASES

Stakeholders
 - Can assign moderators to keep blog family friendly and adhere to policy standards.

Category management
 - Actors: Site Admin, Editor (if permitted)
 - Preconditions: user is staff and has admin access.

Post management
 - Actors: Site Admin, Editor
 - Can delete posts deemed offensive/ threatening to community guidelines.

Comment moderation
 - Moderators approve/unapprove, edit, or delete comments in admin.


Last updated: 2025-11-05
"""

from django.contrib import admin

# Register your models here.
from blog.models import Category, Comment, Post


class CategoryAdmin(admin.ModelAdmin):
    """Admin for Category model.

    Business note: See the module-level "ADMIN USE CASES" comment at the
    top of this file for category-management use cases, acceptance
    criteria, and audit notes.
    """
    list_display = ('name',)
    search_fields = ('name',)


class PostAdmin(admin.ModelAdmin):
    """Admin for Post model.

    Business note: See the module-level "ADMIN USE CASES" comment at the
    top of this file for post-management use cases, editorial workflow,
    role-based expectations, and audit requirements.
    """
    list_display = ('title', 'author', 'created_on', 'last_modified')
    list_filter = ('categories', 'created_on', 'author')
    search_fields = ('title', 'body')
    raw_id_fields = ('author',)
    filter_horizontal = ('categories',)


class CommentAdmin(admin.ModelAdmin):
    """Admin for Comment model.

    Business note: See the module-level "ADMIN USE CASES" comment at the
    top of this file for comment moderation workflows, retention policy,
    and audit/logging considerations.
    """
    list_display = ('author', 'post', 'created_on')
    list_filter = ('created_on', 'post')
    search_fields = ('author', 'body')
    raw_id_fields = ('post',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)