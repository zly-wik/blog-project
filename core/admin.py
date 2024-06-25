from django.contrib import admin

from core.models import Blog, Post, User, UserProfile

# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Blog)
admin.site.register(Post)