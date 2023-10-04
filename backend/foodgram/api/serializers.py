from recipe.models import (
    ListOfPurchases, IngredientRecipes, Ingredient,
    Favorite, Recipes, Tag,
)
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.serializers import UserSerializer
from .helper import create_ingredients
from rest_framework.serializers import ValidationError


class IngredientSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientRecipesReadSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id'
    )

    name = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.name'
    )
    units = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.units'
    )

    class Meta:
        model = IngredientRecipes
        fields = ('id', 'name', 'amount', 'units')


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipesReadSerializer(many=True,
                                                  source='ingredients_used')
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = (
            'id', 'author', 'name', 'image', 'text', 'ingredients',
            'tags', 'cooking_time', 'is_favorited', 'is_in_shopping_cart'
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        is_favorited = (
            not user.is_anonymous and
            Favorite.objects.filter(recipe=obj).exists())
        return is_favorited

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        is_in_cart = (
            not user.is_anonymous and
            ListOfPurchases.objects.filter(recipe=obj).exists())
        return is_in_cart


class RecipeWriteSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = IngredientCreateRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = '__all__'

    def validate_ingredients(self, value):
        if not value:
            raise ValidationError({'ingredients': 'Нужно выбрать ингредиент!'})

        ingredients_list = []
        for item in value:
            ingredient_id = item.get('id')
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
        if not value:
            raise ValidationError({'tags': 'Нельзя создать рецепт без тега!'})

        if len(value) != len(set(value)):
            raise ValidationError({'tags': 'Теги не должны повторяться!'})

        return value

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        tags_data = validated_data.pop('tags', [])
        author = validated_data.pop('author')

        recipe = Recipes.objects.create(author=author, **validated_data)
        recipe.tags.set(tags_data)
        create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        ingredients_data = validated_data.pop('ingredients')
        create_ingredients(ingredients_data, instance)
        tags_data = validated_data.pop('tags')
        instance.tags.set(tags_data)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance, context={'request': self.context.get('request')}).data
