from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,GenericAPIView
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from social.models import Post, Comment, UserProfile, Notification,Image
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .serializers import AccountSerializer,PostSerializer,UserProfileSerializer,CommentSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.profile.first_name
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(GenericAPIView):
    serializer_class=AccountSerializer

    def get(self,request:Request):

        return Response({"register":"register"})


    def post(self,request:Request):
        data =request.data

        serializer =self.serializer_class(data=data)


        if serializer.is_valid():
            serializer.save()

            response={
                'message': 'User Created Successfully',
                'data':serializer.data
            }

            return Response(data=response,status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(RetrieveUpdateDestroyAPIView):
    queryset =UserProfile.objects.all()
    serializer_class =UserProfileSerializer
    lookup_field ='pk'

class PostListCreateView(LoginRequiredMixin, ListCreateAPIView):

    queryset=Post.objects.all()
    serializer_class =PostSerializer


    # def  perform_create(self, serializer):
    #     uploaded_images =serializer.pop("uploaded_images")
    #     post =Post.objects.create(**serializer)
    #     serializer.save(author=self.request.user)
    #   #  print('upl',uploaded_images)
    #     print('p',post)
    #     return post
             

class PostRetriveUpdateDeletView(RetrieveUpdateDestroyAPIView):
    queryset=Post.objects.all()
    serializer_class =PostSerializer
    lookup_field='pk'
    
class CommentView(APIView):

    def get(self, request,post_pk, format=None): 
        queryset =Comment.objects.filter(post=post_pk)
        print('query',queryset)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)    


    def post(self, request,post_pk, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SingleCommentView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request,post_pk,pk, format=None): 
        queryset=Comment.objects.filter(Q(post=post_pk )& Q(id=pk))

        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)    


    def post(self, request,pk, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,post_pk, pk, format=None):
        queryset=Comment.objects.filter(Q(post=post_pk )& Q(id=pk))
        serializer = CommentSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_pk, pk, format=None):
        queryset=Comment.objects.filter(Q(post=post_pk )& Q(id=pk))
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AddLikeView(APIView):
    def get(self, request, pk, *args, **kwargs):
    
        return Response({"message": "logged"},status=status.HTTP_200_OK)

    def post(self, request,pk, *args, **kwargs):
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

        if not is_like:
            post.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=post.author, post=post)

        if is_like:
            post.likes.remove(request.user)
        data =post.likes.count()

        return Response({'likes count:',data},status=status.HTTP_200_OK)

class AddDisLikeView(APIView):
    def get(self, request, pk, *args, **kwargs):

        return Response({"message": "logged"},status=status.HTTP_200_OK)
    
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
        data =post.dislikes.count()

        return Response({'dislikes count:',data},status=status.HTTP_200_OK)

class AddCommentLikeView(APIView):
    def get(self, request, pk, *args, **kwargs):

        return Response({"message": "logged"},status=status.HTTP_200_OK)

    def post(self, request,post_pk, pk, *args, **kwargs):
        comment=Comment.objects.get(Q(post=post_pk )& Q(id=pk))
       

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
            #notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=comment.author, comment=comment)

        if is_like:
            comment.likes.remove(request.user)
        data =comment.likes.count()

        return Response({'likes:',data},status=status.HTTP_200_OK)


class AddCommentDisLikeView(APIView):
    def get(self, request, pk, *args, **kwargs):

        return Response({"message": "logged"},status=status.HTTP_200_OK)

    def post(self, request,post_pk, pk, *args, **kwargs):
        comment=Comment.objects.get(Q(post=post_pk )& Q(id=pk))

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

        data =comment.dislikes.count()

        return Response({'dislikes:',data},status=status.HTTP_200_OK)

class AddImageView(APIView):

    parser_classes =(MultiPartParser, FormParser)
 



    def post(self, request,pk, format=None):
        images =request.FILES.getlist('image[]')
        print('data',request.data['name'])
        name= request.data['name']
        post = Post.objects.get(post_id=pk)

        print(name)

        
        for image in images:
            print('image',image)
            img=Image(image=image,host=post,name=name)
            img.save()
            #img=Image.objects.all().last()
            print(img)

            post.image.add(img)

        post.save()
   

        return Response({'received data':' done'})
    
class AddFollowerView(APIView):

    def get(self, request, pk, *args, **kwargs):

        return Response({"message": "logged"},status=status.HTTP_200_OK)

    def post(self, request, pk, *args, **kwargs):
        user =request.user
        profile = UserProfile.objects.get(pk=pk)
        if profile.user == user:
            return Response({"message":"you cant follow your account"})
        profile.followers.add(user)
        count =profile.followers.count()

        #notification = Notification.objects.create(notification_type=3, from_user=request.user, to_user=profile.user)

        return Response({"Followers":  count },status=status.HTTP_200_OK)

class RemoveFollowerView(APIView):

    def get(self, request, pk, *args, **kwargs):

        return Response({"message": "logged"},status=status.HTTP_200_OK)

    def post(self, request, pk, *args, **kwargs):
        user =request.user
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(user)
        count =profile.followers.count()
        #notification = Notification.objects.create(notification_type=3, from_user=request.user, to_user=profile.user)
        return Response({"Followers":  count},status=status.HTTP_200_OK)