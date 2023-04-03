from rest_framework import serializers
from django.utils import timezone
from myauth.models import myUser
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from core.models import Post, UserProfile,Image

class AccountSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = myUser
        fields = ["email","username", "first_name", "last_name", "password"]

    def validate(self, attrs):
        email_exist = myUser.objects.filter(email=attrs["email"]).exists()
        if email_exist:
            raise ValidationError("Email has already been used")
        
        username_exist = myUser.objects.filter(username=attrs["username"]).exists()
        if username_exist:
            raise ValidationError("username has already been used")
        
        return super().validate(attrs)
    


    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["image", "post"]


class PostSerializer(serializers.ModelSerializer):
    author_picture = serializers.SerializerMethodField(read_only=True)
    author_name = serializers.SerializerMethodField(read_only=True)
    shared_user_name = serializers.SerializerMethodField(read_only=True)
    shared_user_username = serializers.SerializerMethodField(read_only=True)
    shared_user_email = serializers.SerializerMethodField(read_only=True)
    shared_user_picture = serializers.SerializerMethodField(read_only=True)
    author_email = serializers.SerializerMethodField(read_only=True)
    author_username = serializers.SerializerMethodField(read_only=True)
    post_images = serializers.ListField(child=serializers.ImageField(max_length=None, use_url=True), required=False)
    total_likes = serializers.SerializerMethodField(read_only=True)
    liked_by_user = serializers.SerializerMethodField(read_only=True)
    images = ImageSerializer(many=True, read_only=True)


    class Meta:
        model = Post
        fields = [
            "post_id",
            "body",
            "expiration",
            "author",
            "author_name",
            "author_username",
            "shared_body",
            "shared_on",
            "images",
            "post_images",
            "shared_user_name",
            "shared_user_username",
            "shared_user_email",
            "shared_user_picture",
            "author_email",
            "author_picture",
            "total_likes",
            "liked_by_user",
            "created_on",
            "original_post_id",
        ]

 
    def get_total_likes(self, obj):
        return obj.likes.count()
    
    def get_liked_by_user(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(first_name=user).exists()
        return False
        
    def get_shared(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.shared_user.filter(first_name=user).exists()
        return False
        

    def get_author_picture(self, obj):
        return str(obj.author.profile.picture)

    def get_author_name(self, obj):
        return str(obj.author.first_name)
    
    def get_shared_user_name(self, obj):
        if obj.shared_user:
          return str(obj.shared_user.first_name)
        
    def get_shared_user_email(self, obj):
        if obj.shared_user:
          return str(obj.shared_user.email)
    
    def get_shared_user_username(self, obj):
        if obj.shared_user:
          return str(obj.shared_user.username)
    def get_shared_user_picture(self, obj):
        if obj.shared_user:
          return str(obj.get_shared_user_picture())

    def get_author_email(self, obj):
        return str(obj.author.email)
    def get_author_username(self, obj):
        return str(obj.author.username)

    def create(self, validated_data):
        user =self.context.get("request").user

        if validated_data.get('images') is None:
            print('none')
            post = Post.objects.create(body=validated_data["body"], author=user)    
            print('post',post)       
            return post

            
        print('yed')
        post_images =validated_data.pop('images')
        post = Post.objects.create(body=validated_data["body"], author=user)
    
        for image in post_images.values():
                Image.objects.create(image=image,post=post )
                print(image)
        return post
    

               
        
    
    


class UserProfileSerializer(serializers.ModelSerializer):


    class Meta:
        model = UserProfile
        fields = [
            "user",
            "bio",
            "birth_date",
            "location",
            "picture",
            "followers",
            "followings",
            "country",
            "favourite_club",
        ]



