# In blog/views.py
from rest_framework import generics, permissions


from .models import Post, NewsletterSubscription
from .serializers import PostListSerializer, PostDetailSerializer, NewsletterSubscriptionSerializer

class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [permissions.AllowAny]

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug' # Fetch post by its slug instead of ID
    permission_classes = [permissions.AllowAny]

class NewsletterSubscribeView(generics.CreateAPIView):
    queryset = NewsletterSubscription.objects.all()
    serializer_class = NewsletterSubscriptionSerializer
    permission_classes = [permissions.AllowAny]