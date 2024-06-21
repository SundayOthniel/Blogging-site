from django.contrib import admin
from .models import BloggerSignup, BloggerContent, ProfilePicture

admin.site.register(BloggerSignup)
admin.site.register(BloggerContent)
admin.site.register(ProfilePicture)