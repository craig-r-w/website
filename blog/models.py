from django.conf import settings
from django.db import models
from django.utils import timezone

# Django automatically assigns a primary key field 'id'.
class ImageStorage(models.Model):
    # The name and type of the file within static (max of 256 characters)
    # e.g. test_image.png
    name = models.CharField(max_length=256, verbose_name="Filename")

    # String value of a ImageStorage
    def __str__(self):
        return self.name

# Django automatically assigns a primary key field 'id'.
class Post(models.Model):
    # Set the author to the user currently logged in.
    # ForeignKey is used as it is a link to antother model (the User model).
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Store the title with a maximum of 200 characters.
    title = models.CharField(max_length=200, verbose_name="Title")
    
    # Store the content of the blog post into a variable length text field.
    content = models.TextField(verbose_name="Content", blank=True)

    # Set the default value to the current time and set its display name to 'Created Date'.
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Date Created")
    
    # Allow the published_date to be blank and null, and set its display name to 'Published Date'.
    published_date = models.DateTimeField(blank=True, null=True, verbose_name="Date Published")

    # The image to be displayed on the post.
    image = models.ForeignKey(ImageStorage, on_delete=models.CASCADE)

    # Added to prevent Virtual Studio Code from flagging accessing 'objects' as an error.
    objects = models.Manager()

    # Called when a Post is published: so change the published date to the current date.
    def publish(self, author):
        self.published_date = timezone.now()
        self.author = author
        self.save()

    # Used to set the author (as this field cannot be blank).
    def setAuthor(self, author):
        self.author = author
        self.save()

    # String value of a Post
    def __str__(self):
        return self.title
    