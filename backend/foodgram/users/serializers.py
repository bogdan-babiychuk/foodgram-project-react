from rest_framework import serializers
from .models import User
from recipe.models import Follow, Recipes
from api.helper import BaseRecipeSerializer

class UserSerializer(serializers.ModelSerializer):
    """Сериализтор для юзера"""
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',)

    def is_subscribed(self, obj):
        """Подписан или нет"""
        user = self.context.get('request').user
        if not user.is_anonymous:
            return user.follower.filter(author=obj).exists()
        return False

class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя, с уникальным полем password"""
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class FavoriteFollowSerializer(BaseRecipeSerializer):
    """api/helper.py"""
    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')

class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор Модели Follow"""
    id = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'email',
                  'username', 'first_name',
                  'last_name', 'is_sibscribed',
                  'recipes', 'recipes_count')
    
    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return user.follower.filter(author=obj).exists()
        return False

    def get_recipes(self, obj):
        """Этот метод вообще не понимаю, но мне сказали его добавить в пачке"""
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = Recipes.objects.filter(author=obj.author)
        if limit and limit.isdigit():
            recipes = recipes[:int(limit)]
        serializer = FavoriteFollowSerializer(recipes, many=True)
        return serializer.data
    
    def get_recipes_count(self, obj):
        return Recipes.objects.filter(author=obj.author).count()
