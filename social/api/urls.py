from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import (
    RegisterView,
    MyTokenObtainPairView,
    PostCreateView,
    PostRetriveUpdateDeletView,
    UserProfileView,
    AddLikeView,
    AddFollowingView,
    ListFollowersView,
    ListFollowingView,
    AddCommentLikeView,
    AddCommentDisLikeView,
    listPost,
    ResharedPost
)

app_name ='api'

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", listPost.as_view(), name="list-create"),
    path("create/", PostCreateView.as_view(), name="create"),
    path("post/<str:pk>", PostRetriveUpdateDeletView.as_view(), name="post-detail"),
    path("profile/<int:pk>", UserProfileView.as_view(), name="profile"),
    path("profile/add-follow/<str:pk>", AddFollowingView.as_view(), name="add-following"),
    path("profile/followers", ListFollowersView.as_view(), name="list-followers"),
    path("profile/following", ListFollowingView.as_view(), name="list-following"),

    path("post/like/<str:pk>/", AddLikeView.as_view(), name="post-like"),
    path("post/reshare/<str:pk>/", ResharedPost.as_view(), name="post-rehare"),
    path(
        "post/comment/<str:post_pk>/<int:pk>/like",
        AddCommentLikeView.as_view(),
        name="like-comment",
    ),
    path(
        "post/comment/<str:post_pk>/<int:pk>/dislike",
        AddCommentDisLikeView.as_view(),
        name="dislike-comment",
    ),
]
