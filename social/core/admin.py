from django.contrib import admin
from .models import Post,UserProfile,Comment,ReplyComment,Image

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(ReplyComment)
