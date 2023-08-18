from django.urls import path, include
from rest_framework import routers

import api.views

router = routers.DefaultRouter()
router.register(
    'groups',
    api.views.GroupViewSet,
    basename='groups',
)

router.register(
    'posts',
    api.views.PostViewSet,
    basename='posts',
)

router.register(
    r'posts/(?P<post_id>\d+)/comments',
    api.views.CommentViewSet,
    basename='comments',
)

router.register(
    'follow',
    api.views.FollowViewSet,
    basename='follow',
)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
