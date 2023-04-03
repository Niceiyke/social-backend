import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


from.manager import PostManager,ProfileManager
    
class MyUUIDModel(models.Model):
	id = models.UUIDField(
		primary_key = True,
		default = uuid.uuid4,
		editable = False)
	# other fields
User= get_user_model()


class UserProfile(models.Model):
    user=models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE,db_index=True)
    bio =models.TextField(max_length=500, blank=True, null=True)
    birth_date=models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/default.png', blank=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    followings = models.ManyToManyField(User, blank=True, related_name='following')
    country =models.CharField(max_length=50,null=True,blank=True)
    favourite_club =models.CharField(max_length=50,null=True,blank=True)
    verified =models.BooleanField(default=False)


    objects =ProfileManager()
   
    def __str__(self):
        return self.user.first_name
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    created_at = models.DateTimeField( auto_now_add=True,db_index=True)


class Post(models.Model): 
    post_id =models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    author =models.ForeignKey(User,on_delete=models.CASCADE,related_name='authors',db_index=True)
    body =models.CharField(max_length=240,db_index=True)
    shared_body=models.CharField(max_length=240,blank=True,null=True)
    shared_on =models.DateTimeField(auto_now=True,db_index=True)
    original_post_id = models.CharField(max_length=60,blank=True,null=True)
    shared_user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True, related_name='shared_users',db_index=True)
    created_on = models.DateTimeField(default=timezone.now,db_index=True)
    modified_on= models.DateTimeField(auto_now=True,db_index=True)
    expiration= models.DateTimeField(blank=True ,null=True,db_index=True)
    likes = models.ManyToManyField(User, through='Like', related_name='liked_posts',blank=True)
  

    objects=PostManager()

    class Meta:
        ordering=['-created_on','-shared_on']

    def __str__(self):
        return self.body[:20]

    def get_shared_user_name(self):
        shared_user_name = self.shared_user.first_name 
        return shared_user_name

    def get_author_picture(self):
        author_picture = self.author.profile.picture
        return author_picture
    
    def get_shared_user_picture(self):
        shared_user_picture = self.shared_user.profile.picture
        return shared_user_picture


        


class Image(models.Model):
    image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='images')
    

    
@receiver(post_save,sender=User)
def ProfileCreate(sender,instance,created,*args, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
            
            print('profile created')


