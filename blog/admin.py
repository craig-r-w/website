from django.contrib import admin
from .models import Post, ImageStorage

# Register your models here.

# Register the Post model.
admin.site.register(Post)
admin.site.register(ImageStorage)