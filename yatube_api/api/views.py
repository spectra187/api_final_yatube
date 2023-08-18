from rest_framework import filters, permissions, viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

import api.serializers
from api.permissions import IsAuthorOrReadOnly
from posts.models import Group, Post


API_PERMISSIONS = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = api.serializers.GroupSerializer
    queryset = Group.objects.all()


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = api.serializers.PostSerializer
    permission_classes = API_PERMISSIONS
    pagination_class = LimitOffsetPagination
    queryset = Post.objects.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = api.serializers.CommentSerializer
    permission_classes = API_PERMISSIONS

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = api.serializers.FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
