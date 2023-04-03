from django.db import models
from django.contrib.auth import get_user_model


User =get_user_model()

# Create your models here.
class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    reply =models.ManyToManyField("ReplyComment",blank=True,related_name="replies")


    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created_on').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False



    class Meta:
        ordering=['-created_on']

class ReplyComment(models.Model):
    reply = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='reply_likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='reply_dislikes')
    parent = models.ForeignKey('Comment', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
 
    @property
    def children(self):
        return ReplyComment.objects.filter(parent=self).order_by('-created_on').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False



    class Meta:
        ordering=['-created_on']

