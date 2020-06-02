from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .models import Post

from django.core.paginator import Paginator

# The home view.
def home(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    paginator = Paginator(posts, 3) # Show 3 posts per page.

    # GET the specified page number.
    # e.g. ?page=1
    page_number = request.GET.get('page')

    # Select the relevant page.
    page = paginator.get_page(page_number)

    return render(request, 'blog/display_posts.html', {'posts': posts, 'page': page})