from django.db import models
from itertools import chain
import random



class PostQuerySet(models.QuerySet):    
    def get_user_feed(self,user,followings):
        follwings_post = []
        for profile in followings:
            profile_posts = self.filter(author=profile)
            for post in profile_posts:
                follwings_post.append(post)
        user_post = self.filter(author=user)
        queryset = list(chain(user_post, follwings_post))
        random.shuffle(queryset)
        return queryset
    
    def get_user_post(self,user):
        return self.filter(author=user)

class ProfileQueryset(models.QuerySet):
    def get_user_followers(self,pk):
        profiles=[]
        followers = list(self.get(pk=pk).followers.all())
        for user in followers:
            profile=self.get(pk=user)
            profiles.append(profile)     
        return profiles


    def get_user_followings(self,pk):
        profiles=[]
        followings = list(self.get(pk=pk).followings.all())
        for user in followings:
            profile=self.get(pk=user)
            profiles.append(profile)     
        return profiles
    
    def get_all_user_profile(self):
        all_users_profile = self.values_list('user',flat=True)
        return list(all_users_profile)

class ProfileManager(models.Manager):
    def get_queryset(self):
        return ProfileQueryset(self.model,using=self._db)
    
    def get_user_following(self,pk):
        return self.get_queryset().get_user_followings(pk)
    
    def get_user_followers(self,pk):
        return self.get_queryset().get_user_followers(pk)
    
    def get_all_user_profile(self):
        return self.get_queryset().get_all_user_profile()
  
class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model,using=self._db)
    
    def get_user_feed(self,user,followings):
        return self.get_queryset().get_user_feed(user,followings)
    
    def get_user_post(self,user):
        return self.get_queryset().get_user_post(user)


