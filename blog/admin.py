# In blog/admin.py
from django.contrib import admin
from .models import Post, NewsletterSubscription

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_on')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_on')