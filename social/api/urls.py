from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import (RegisterView,MyTokenObtainPairView,PostListCreateView,
PostRetriveUpdateDeletView,UserProfileView,CommentView,SingleCommentView,AddLikeView,
AddDisLikeView,AddFollowerView,RemoveFollowerView,AddCommentLikeView,AddCommentDisLikeView,AddImageView

)

urlpatterns = [

 path('register/',RegisterView.as_view(),name='register'),
 path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
 path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

 
 path('',PostListCreateView.as_view(),name='list-create'),
 path('post/<str:pk>',PostRetriveUpdateDeletView.as_view(),name='single-post'),
 path('profile/<int:pk>',UserProfileView.as_view(),name='profile'),
 path('profile/<int:pk>/follow',AddFollowerView.as_view(),name='follow'),
 path('profile/<int:pk>/unfollow',RemoveFollowerView.as_view(),name='unfollow'),
 path('post/comment/<str:post_pk>',CommentView.as_view(),name='list-comment'),
 path('post/comment/<str:post_pk>/<int:pk>',SingleCommentView.as_view(),name='single-comment'),
 path('post/<str:pk>/like/', AddLikeView.as_view(), name='post-like'),
 path('post/<str:pk>/dislike/', AddDisLikeView.as_view(), name='post-dislike'),
 path('post/<str:pk>/image/', AddImageView.as_view(), name='post-image'),
 path('post/comment/<str:post_pk>/<int:pk>/like',AddCommentLikeView.as_view(),name='like-comment'),
 path('post/comment/<str:post_pk>/<int:pk>/dislike',AddCommentDisLikeView.as_view(),name='dislike-comment'),






]
