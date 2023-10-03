from recipe .models import (List_Of_Purchases, IngredientRecipes, Ingredient,
                            Favorite, Recipes, Tag,)
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.serializers import UserSerializer
from .helper import create_ingredients


class IngredientSerializer(serializers.ModelSerializer):
    """
    Базовый Сериализатор для ингредиентов
    http://127.0.0.1:8000/api/v1/ingredients/
    """
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientCreateRecipeSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipes
        fields = ('id', 'amount',)


class TagSerializer(serializers.ModelSerializer):
    """
    Базовый Сериализатор для тегов.
    http://127.0.0.1:8000/api/v1/tags/
    """
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientRecipesReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вспомогательной модели IngredientRecipes
    благодаря source, можно получить ПРАВИЛЬНОE ID ингредиента
    и также строковое представление для название ингредиента
    """
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source='ingredient.id'
    )

    name = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.name'
    )
    units = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.units')

    class Meta:
        model = IngredientRecipes
        fields = ('id', 'name', 'amount', 'units')


class RecipeReadSerializer(serializers.ModelSerializer):
    """
    GET запрос для получения объектов модели Recipes
    http://127.0.0.1:8000/api/v1/recipes/
    """
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipesReadSerializer(many=True,
                                                  source='ingredients_used')
    image = Base64ImageField()
    tags = TagSerializer(read_only=True,
                         many=True)

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = ('id', 'author',
                  'name', 'image',
                  'text', 'ingredients',
                  'tags', 'cooking_time',
                  'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Favorite.objects.filter(recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return List_Of_Purchases.objects.filter(recipe=obj).exists()
        return False


class RecipeWriteSerializer(serializers.ModelSerializer):
    """
    Запись и обновление объектов модели Recipes
    http://127.0.0.1:8000/api/v1/recipes/
    """
    """create/update для рецептов"""

    author = UserSerializer(read_only=True)
    ingredients = IngredientCreateRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = '__all__'

    def validate_ingredients(self, value):
        """Валидация ингредиентов"""
        ingredients = value
        if not ingredients:
            return serializers.ValidationError({'ingredients':
                                                'Нужно выбрать ингредиент!'})

        ingredients_list = []
        for item in ingredients:
            ingredient_id = item.get('id')
            if not ingredient_id:
                raise serializers.ValidationError({
                    'ingredients': 'Каждый ингредиент должен иметь ID!'})

            try:
                ingredient = Ingredient.objects.get(id=ingredient_id)
            except Ingredient.DoesNotExist:
                raise serializers.ValidationError(
                    {'ingredients':
                      f'Ингредиент с ID {ingredient_id} не существует!'})

            if ingredient in ingredients_list:
                raise serializers.ValidationError({
                    'ingredients': 'Ингредиенты не должны повторяться!'})

            ingredients_list.append(ingredient)
        return value

    def validate_tags(self, value):
        """Валидация тегов"""
        tags = value
        if not tags:
            raise serializers.ValidationError({
                'tags': 'Нельзя создать рецепт без тега!'})

        if len(tags) != len(set(tags)):
            raise serializers.ValidationError({
                'tags': 'Теги не должны повторяться!'})

        return tags

    def create(self, validated_data):
        """Создание рецепта с помощию доп функции из helper.py """
        ingredients_data = validated_data.pop('ingredients', [])
        tags_data = validated_data.pop('tags', [])
        author = validated_data.pop('author')

        recipe = Recipes.objects.create(author=author, **validated_data)
        recipe.tags.set(tags_data)
        create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        """Обновление существующей записи"""
        instance.ingredients.clear()
        ingredients_data = validated_data.pop('ingredients')
        create_ingredients(ingredients_data, instance)
        tags_data = validated_data.pop('tags')
        instance.tags.set(tags_data)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance, context={'request': self.context.get('request')}).data
