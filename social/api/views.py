from itertools import chain
import random
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    GenericAPIView,
)
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from core.models import Post, Comment, UserProfile, Image
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .serializers import (
    AccountSerializer,
    PostSerializer,
    UserProfileSerializer,
    CommentSerializer,
)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["email"] = user.email
        token["first_name"] = user.profile.first_name
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(GenericAPIView):
    serializer_class = AccountSerializer

    def get(self, request: Request):

        return Response({"register": "register"})

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {"message": "User Created Successfully", "data": serializer.data}

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = "pk"


class PostCreateView(LoginRequiredMixin, CreateAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # def  perform_create(self, serializer):
    #     uploaded_images =serializer.pop("uploaded_images")
    #     post =Post.objects.create(**serializer)
    #     serializer.save(author=self.request.user)
    #   #  print('upl',uploaded_images)
    #     print('p',post)
    #     return post


class listPost(APIView):
    def get(self, request):
        follwings_post = []
        user = request.user
        followings = UserProfile.objects.get(user=user).following.all()

        for profile in followings:
            profile_posts = Post.objects.filter(author=profile)
            for post in profile_posts:
                follwings_post.append(post)

        user_post = Post.objects.filter(author=user)
        queryset = list(chain(user_post, follwings_post))
        print(len(queryset))
        random.shuffle(queryset)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


class PostRetriveUpdateDeletView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "pk"


class CommentView(APIView):
    def get(self, request, post_pk, format=None):
        queryset = Comment.objects.filter(post=post_pk)
        print("query", queryset)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, post_pk, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleCommentView(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, post_pk, pk, format=None):
        queryset = Comment.objects.filter(Q(post=post_pk) & Q(id=pk))

        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, post_pk, pk, format=None):
        queryset = Comment.objects.filter(Q(post=post_pk) & Q(id=pk))
        serializer = CommentSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_pk, pk, format=None):
        queryset = Comment.objects.filter(Q(post=post_pk) & Q(id=pk))
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddLikeView(APIView):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(post_id=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)
        data = post.likes.count()

        return Response({"likes count:", data}, status=status.HTTP_200_OK)


class AddDisLikeView(APIView):
    def get(self, request, pk, *args, **kwargs):

        return Response({"message": "logged"}, status=status.HTTP_200_OK)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(post_id=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)
        data = post.dislikes.count()

        return Response({"dislikes count:", data}, status=status.HTTP_200_OK)


class AddCommentLikeView(APIView):
    def get(self, request, pk, *args, **kwargs):

        return Response({"message": "logged"}, status=status.HTTP_200_OK)

    def post(self, request, post_pk, pk, *args, **kwargs):
        comment = Comment.objects.get(Q(post=post_pk) & Q(id=pk))

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)
            # notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=comment.author, comment=comment)

        if is_like:
            comment.likes.remove(request.user)
        data = comment.likes.count()

        return Response({"likes:", data}, status=status.HTTP_200_OK)


class AddCommentDisLikeView(APIView):
    def get(self, request, pk, *args, **kwargs):

        return Response({"message": "logged"}, status=status.HTTP_200_OK)

    def post(self, request, post_pk, pk, *args, **kwargs):
        comment = Comment.objects.get(Q(post=post_pk) & Q(id=pk))

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)

        if is_dislike:
            comment.dislikes.remove(request.user)

        data = comment.dislikes.count()

        return Response({"dislikes:", data}, status=status.HTTP_200_OK)


class AddImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, pk, format=None):
        images = request.FILES.getlist("image[]")
        print("data", request.data["name"])
        name = request.data["name"]
        post = Post.objects.get(post_id=pk)
        for image in images:
            print("image", image)
            img = Image(image=image, host=post, name=name)
            img.save()
            # img=Image.objects.all().last()
            print(img)

            post.image.add(img)

        post.save()

        return Response({"received data": " done"})


class AddFollowingView(APIView):        
    def post(self, request, pk, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects.get(pk=pk)
        profile_follower = UserProfile.objects.get(user=user)
        if profile.user == user:
            return Response("you cannot follow ur own account")

        followings = profile.following.all()
        for follower in followings:
            if follower == user:
                profile.following.remove(user)
                profile_follower.followers.remove(profile.user)
                count = profile.following.count()
                return Response({"Followeing": count}, status=status.HTTP_200_OK)
        profile.following.add(user)
        profile_follower.followers.add(profile.user)
        count = profile.following.count()
        # notification = Notification.objects.create(notification_type=3, from_user=request.user, to_user=profile.user)
        return Response({"Followeing": count}, status=status.HTTP_200_OK)


class ListFollowersView(APIView):
    def get(self, request, pk, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects.get(pk=pk)
        count = profile.followers.count()
        return Response({"Followers": count}, status=status.HTTP_200_OK)
    
class ListFollowingView(APIView):
    def get(self, request, pk, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects.get(pk=pk)
        count = profile.following.count()
        return Response({"Following": count}, status=status.HTTP_200_OK)
