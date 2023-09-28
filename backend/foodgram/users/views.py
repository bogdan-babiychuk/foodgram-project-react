from django.shortcuts import render
from .serializers import UserCreateSerializer, UserSerializer
from .models import User
from rest_framework.response import Response
from recipe.models import Follow
from djoser.views import UserViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated    
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import status
from .serializers import FollowSerializer

class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def manage_subscriptions(self, request, **kwargs):
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        user = self.request.user
        if request.method == 'POST':
            if user != author:
                follow = Follow.objects.get_or_create(
                    user=user,
                    author=author
                )
                if follow.objects.filter(
                    user=user,
                    author=author
                    ).exists():

                    return  Response({
                        'error': 'Нельзя подписаться повторно'
                    })
                serializer_data = FollowSerializer(
                    author, context={'request': request, }
                )
                
                return Response({'Вы подписались': serializer_data.data},
                    status=status.HTTP_201_CREATED)
            return Response({'error': 'Нельзя подписываться на самого себя'})
        
        if request.method == 'DELETE':
            if not Follow.objects.filter(author=author, user=user).exists():
                return Response(
                    {"error": "Вы не подписаны на этого пользователя."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            Follow.objects.get(author=author).delete()
            return Response('Вы отписались',
                            status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,methods=['get'],permission_classes=[IsAuthenticated])
    def my_subscriptions(self, request):
        """Отображает все подписки пользователя."""
        follows = Follow.objects.filter(user=self.request.user)
        pages = self.paginate_queryset(follows)
        serializer = FollowSerializer(pages,
                                      many=True,
                                      context={'request': request})
        return self.get_paginated_response(serializer.data)   
            



    
