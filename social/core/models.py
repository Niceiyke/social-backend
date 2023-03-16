import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
    
class MyUUIDModel(models.Model):
	id = models.UUIDField(
		primary_key = True,
		default = uuid.uuid4,
		editable = False)
	# other fields
User= get_user_model()


class UserProfile(models.Model):
    user=models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    first_name =models.CharField(max_length=20, blank=True, null=True)
    last_name =models.CharField(max_length=20, blank=True, null=True)
    bio =models.TextField(max_length=500, blank=True, null=True)
    birth_date=models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/default.png', blank=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    country =models.CharField(max_length=50,null=True,blank=True)
    favourite_club =models.CharField(max_length=50,null=True,blank=True)
    
    def __str__(self):
        return self.user.email


class Post(models.Model): 
    post_id =models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    author =models.ForeignKey(User,on_delete=models.CASCADE)
    body =models.CharField(max_length=240)
    image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on= models.DateTimeField(auto_now=True)
    likes =models.ManyToManyField(User,blank=True,related_name='likes',)
    dislikes =models.ManyToManyField(User,blank=True,related_name='dislikes',)
    expiration= models.DateTimeField(null=True)
    comments =models.ManyToManyField('Comment',blank=True,related_name='comments',)



    class Meta:
        ordering=['-created_on']

    def __str__(self):
        return self.body[:20]

    def get_number_of_likes(self):
        number_of_likes = self.likes.count()
        return number_of_likes

    def get_number_of_dislikes(self):
        number_of_dislikes = self.dislikes.count()
        return number_of_dislikes

    def get_author_picture(self):
        author_picture = self.author.profile.picture
        print(author_picture)
        return author_picture

    def get_absolute_url(self):
        return reverse('social:post-detail',args=[self.post_id])


class Image(models.Model):
    image_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE ,related_name='images',blank=True,null=True)

   
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

@receiver(post_save,sender=User)
def ProfileCreate(sender,instance,created,*args, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print('profile created')

