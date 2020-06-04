from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import Post
from .forms import PostForm

from django.core.paginator import Paginator
from django.templatetags.static import static

# The home view- displays blog posts in pages.
def home(request):
    # Select only articles that have been published after the current date.
    # Order by newest first.
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('-published_date')

    # Show 3 posts per page.
    paginator = Paginator(posts, 3)

    # GET the specified page number.
    # e.g. ?page=1
    page_number = request.GET.get('page')

    # Select the relevant page.
    page = paginator.get_page(page_number)

    return render(request, 'blog/display_posts.html', {'page': page})

# Viewing an individual post.
def view_post(request, primary_key):

    # Get the post object based on the provided primary key
    post = get_object_or_404(Post, pk=primary_key)

    # The post info.
    title = post.title
    content = post.content
    author = getStringUserName(post.author)
    image_url = static("images/" + post.image.name)
    published = post.published_date.date()

    return render(request, 'blog/display_post.html', {'title': title, 'content': content, 'author': author, 'published': published, "image_url": image_url, })

# Create a new post.
def create_post(request):
    # A default blank form.
    form = PostForm()

    # See if form data has been sent.
    if request.method == "POST":
        # Get the form data.
        form = PostForm(request.POST)

        # !!!
        # PASS IN THE CREATED_DATE as a hidden input?
        # Select fisrt radio element by id
        # !!!

        if form.is_valid():
            # commit=False to make changes before the Post is saved.
            post = form.save(commit=False)

            # If the button named 'publish' is pressed.
            if 'publish' in request.POST:
                post.publish(request.user)
            else:
                # This cannot be blank so it needs to be set now.
                post.setAuthor(request.user)

            # Redirect to the relevant edit page.
            return redirect(edit_post, primary_key=post.pk)

    # Basic info.
    user = getStringUserName(request.user)
    created_date = timezone.now()

    return render(request, 'blog/create_post.html', {'form': form, 'user': user, 'created_date': created_date})


def edit_post(request, primary_key):
    post = get_object_or_404(Post, pk=primary_key)
    form = PostForm(instance=post)

    # If chenges to the form have been submitted.
    if request.method == "POST":
        # Form data has been sent.
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            # commit=False to make changes before the Post is saved.
            post = form.save(commit=False)
            post.author = request.user

           # If the button named 'publish' is pressed.
            if ('publish' in request.POST) or ('republish' in request.POST):
                post.published_date = timezone.now()
                post.save()
                # Redirect back to the home page.
                # return redirect(home)
                # return redirect(edit_post, primary_key=post.pk)
            elif 'unpublish' in request.POST:
                post.published_date = None

            # Save the Post.
            post.save()

    title = post.title
    user = getStringUserName(post.author)
    created_date = post.created_date.date()
    published_date = None
    if post.published_date:
        published_date = post.published_date  # .date()

    return render(request, 'blog/create_post.html', {'title': title, 'form': form, 'user': user, 'created_date': created_date, 'published_date': published_date})


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
