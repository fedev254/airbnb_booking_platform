# In blog/urls.py
from django.urls import path
from .views import PostListView, PostDetailView, NewsletterSubscribeView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('subscribe/', NewsletterSubscribeView.as_view(), name='newsletter-subscribe'),
]