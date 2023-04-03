from django.contrib import admin
from .models import Post,UserProfile,Image

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Image)

