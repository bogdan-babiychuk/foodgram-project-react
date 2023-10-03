from rest_framework import serializers
from .models import User
from recipe.models import Follow, Recipes


class UserSerializer(serializers.ModelSerializer):
    """Сериализтор для юзера"""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        """Подписан или нет"""
        user = self.context.get('request').user
        if not user.is_anonymous:
            # Проверяем, что пользователь не подписан на самого себя
            if user != obj:
                return Follow.objects.filter(user=user, author=obj).exists()
        return False


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя, с уникальным полем password"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class FavoriteFollowSerializer(serializers.ModelSerializer):
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
                  'last_name', 'is_subscribed',
                  'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        """Подписан или нет"""
        user = self.context.get('request').user
        if not user.is_anonymous:
            # Проверяем, что пользователь не подписан на самого себя
            if user != obj:
                return Follow.objects.filter(user=user, author=obj).exists()
        return False

    def get_recipes(self, obj):
        """Получение рецептов автора, на которого подписан пользователь"""
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipe.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = FavoriteFollowSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipes.objects.filter(author=obj).count()
