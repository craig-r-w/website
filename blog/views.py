from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from .models import Post

from django.core.paginator import Paginator
from django.templatetags.static import static

# The home view.
def home(request):    
    # Select only articles that have been published after the current date.
    # Order by newest first.
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    paginator = Paginator(posts, 3) # Show 3 posts per page.

    # GET the specified page number.
    # e.g. ?page=1
    page_number = request.GET.get('page')

    # Select the relevant page.
    page = paginator.get_page(page_number)

    return render(request, 'blog/display_posts.html', {'page': page})

# Viewing an individual post.
def view_post(request, private_key):

    post = get_object_or_404(Post, pk=private_key)

    title = post.title
    content = post.content
    author = ""
    image_url = static("images/" + post.image.name)
    published = post.published_date.date()

    if(post.author.first_name):
        # The first name field is not blank, so use that.
        author = post.author.first_name.capitalize()
        if(post.author.last_name):
            # Add on the second name if that exists.
            author += " " + post.author.last_name.capitalize()
    else:
        # Use the username.
        author = post.author.username.capitalize()

    return render(request, 'blog/display_post.html', {'title':title, 'content': content, 'author':author, 'published': published, "image_url": image_url, })