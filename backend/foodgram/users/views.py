from .serializers import UserSerializer, FollowSerializer
from .models import User
from rest_framework.response import Response
from recipe.models import Follow
from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import status


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, **kwargs):
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        user = self.request.user
        if request.method == 'POST':
            if user != author:
                Follow.objects.get_or_create(
                    user=user,
                    author=author
                )
                if Follow.objects.filter(
                                        user=user,
                                        author=author
                                        ).exists():

                    return Response({
                        'error': 'Нельзя подписаться повторно'
                    })
                serializer_data = FollowSerializer(
                    author, context={'request': request}
                )

                return Response({'Вы подписались': serializer_data.data},
                                status=status.HTTP_201_CREATED)
            return Response({'error': 'Нельзя подписываться на самого себя'})

        elif request.method == 'DELETE':
            follow_delete = Follow.objects.filter(
                                                 author=author,
                                                 user=user
                                                 ).first()
            if follow_delete:
                follow_delete.delete()
                return Response('Вы отписались',
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {"error": "Вы не подписаны на этого пользователя."},
                    status=status.HTTP_400_BAD_REQUEST
                )

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        queryset = User.objects.filter(followed__user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)
