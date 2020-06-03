from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from .models import Post
from .forms import PostForm

from datetime import datetime

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
    author = getStringUserName(post.author)
    image_url = static("images/" + post.image.name)
    published = post.published_date.date()

    return render(request, 'blog/display_post.html', {'title':title, 'content': content, 'author':author, 'published': published, "image_url": image_url, })

def create_post(request):
    form = PostForm()
    user = getStringUserName(request.user)
    created_date = datetime.now().date()

    return render(request, 'blog/create_post.html', {'form': form, 'user': user, 'created_date': created_date})

# Takes in a user object and attempts to display it nicely as a string.
def getStringUserName(user):
    name = ""

    if(user.first_name):
        # The first name field is not blank, so use that.
        name = user.first_name.capitalize()
        if(user.last_name):
            # Add on the second name if that exists.
            name += " " + user.last_name.capitalize()
    else:
        # Use the username.
        name = user.username.capitalize()
    
    return name