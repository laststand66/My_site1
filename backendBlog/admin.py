from django.contrib import admin
from .models import MainUser, Article, Category, Comment

class AdminPosts(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'pub_date')
    list_filter = ('status',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug':('title',)}


class AdminComments(admin.ModelAdmin):
    list_display = ('name', 'body', 'article', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('name', 'body')




admin.site.register(MainUser)
admin.site.register(Article, AdminPosts)
admin.site.register(Category)
admin.site.register(Comment, AdminComments)
