from rest_framework.generics import (
    CreateAPIView, ListAPIView,
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
from rest_framework.permissions import IsAuthenticated
from core.models import Post,UserProfile,Image
from myauth.models import myUser
from .serializers import (
    AccountSerializer,
    PostSerializer,
    UserProfileSerializer,
 
)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["id"] = user.id
        token["email"] = user.email
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["username"] = user.username
        token["profile_picture"] = str(user.profile.picture)
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(GenericAPIView):
    serializer_class = AccountSerializer

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


class PostCreateView( CreateAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class listPost(ListAPIView):

    queryset = Post.objects.all()
     
    serializer_class = PostSerializer

    def get_queryset(self):
        qs=super().get_queryset()
        return (qs)
        

class ResharedPost(APIView):

    def post(self,request,pk):
        original_post=Post.objects.get(post_id=pk)
        print(original_post.post_id)
        images=original_post.images.all()

        new_post = Post(shared_body=request.data['shared_body'],body=original_post.body,
                        author=original_post.author,created_on=original_post.created_on,
                        shared_user=request.user,original_post_id=str(original_post.post_id))        
        new_post.save()

        for image in images:
            new_post.images.add(image)
            new_post.save()

     
       
        return Response({"message":'reshared'})


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


        is_like = False

        for like in post.favourite.all():        
            if str(like) == str(request.user):
                is_like = True
                break

        if is_like:
            
            post.favourite.remove(request.user)
            data = post.favourite.count()
            return Response (data,status=status.HTTP_200_OK)

        else:
            post.favourite.add(request.user)
            data = post.favourite.count()
            return Response (data,status=status.HTTP_200_OK)




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


class AddFollowingView(APIView):
    def post(self, request, pk, *args, **kwargs):
        current_user = request.user
        profile = UserProfile.objects.get(pk=current_user.id)
        profile_follower = UserProfile.objects.get(user=pk)
        user_to_follow = myUser.objects.get(pk=pk)

        if current_user == user_to_follow:
            return Response(
                {"message": "you cannot follow your own account"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        followings = profile.followings.all()
        for follower in followings:
            if follower == user_to_follow:
                profile.followings.remove(pk)
                profile_follower.followers.remove(current_user)
                count = profile.followings.count()
                return Response({"Following": count}, status=status.HTTP_202_ACCEPTED)
        profile.followings.add(pk)
        profile_follower.followers.add(current_user)
        count = profile.followings.count()
        return Response({"Following": count}, status=status.HTTP_200_OK)


class ListFollowersView(APIView):
    def get(self, request, *args, **kwargs):
        followers = UserProfile.objects.get_user_followers(pk=request.user.id)
        serializer = UserProfileSerializer(followers, many=True)
        count = len(followers)
        return Response({"followers": serializer.data}, status=status.HTTP_200_OK)


class ListFollowingView(APIView):
    def get(self, request, *args, **kwargs):
        current_user = UserProfile.objects.filter(pk=request.user.id)
        profiles = []
        following = UserProfile.objects.get_user_following(pk=request.user.id)

        all_user = UserProfile.objects.get_all_user_profile()

        for user in all_user:
            profile = UserProfile.objects.get(pk=user)
            profiles.append(profile)

        sugested_profiles_to_follow = [
            user for user in profiles if user not in following
        ]
        final_suggested_profile_to_follow = [
            user
            for user in sugested_profiles_to_follow
            if user not in list(current_user)
        ]

        serializer = UserProfileSerializer(following, many=True)
        return Response({"following": serializer.data}, status=status.HTTP_200_OK)
