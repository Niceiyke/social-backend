from rest_framework import serializers
from myauth.models import myUser
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from core.models import Post, UserProfile, Comment, Image


class AccountSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = myUser
        fields = ["email", "first_name", "last_name", "password"]

    def validate(self, attrs):
        email_exist = myUser.objects.filter(email=attrs["email"]).exists()
        if email_exist:
            raise ValidationError("Email has already been used")
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
    num_likes = serializers.SerializerMethodField(read_only=True)
    num_dislikes = serializers.SerializerMethodField(read_only=True)
    author_picture = serializers.SerializerMethodField(read_only=True)
    author_name = serializers.SerializerMethodField(read_only=True)
    author_email = serializers.SerializerMethodField(read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=1000000,
            allow_empty_file=False,
            use_url=False,
        ),
        write_only=True,
    )

    class Meta:
        model = Post
        fields = [
            "post_id",
            "body",
            "expiration",
            "author",
            "author_name",
            "images",
            "uploaded_images",
            "author_email",
            "author_picture",
            "likes",
            "num_likes",
            "num_dislikes",
            "dislikes",
            "created_on",
        ]

    def get_num_likes(self, obj):
        return obj.get_number_of_likes()

    def get_num_dislikes(self, obj):
        return obj.get_number_of_dislikes()

    def get_author_picture(self, obj):
        return str(obj.author.profile.picture)

    def get_author_name(self, obj):
        return str(obj.author.profile.first_name)

    def get_author_email(self, obj):
        return str(obj.author.profile.user.email)

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        uploaded_images = validated_data.pop("uploaded_images")
        post = Post.objects.create(body=validated_data["body"], author=user)
        for image in uploaded_images:
            Image.objects.create(post=post, image=image)

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
            "following",
            "country",
            "favourite_club",
        ]



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
