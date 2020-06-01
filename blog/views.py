from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

# The home view.
def home(request):
    posts = Post.objects.all()

    return render(request, 'blog/display_posts.html', {'posts': posts})