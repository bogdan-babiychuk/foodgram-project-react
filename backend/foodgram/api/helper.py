from rest_framework import serializers
from recipe.models import IngredientRecipes, Ingredient


class BaseRecipeSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для моделей Favorite и List_Of_Purchases."""

    id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='recipes.id',)
    name = serializers.ReadOnlyField(
        read_only=True,
        source='recipes.name',)
    image = serializers.ImageField(
        read_only=True,
        source='recipes.image',)
    coocking_time = serializers.IntegerField(
        read_only=True,
        source='recipe.cooking_time',)

    class Meta:
        abstract = True  # Делаем этот класс абстрактным


def create_ingredients(ingredients, recipe):
    for ingredient_data in ingredients:
        ingredient, _ = Ingredient.objects.get_or_create(
            id=ingredient_data.get('id'))
        IngredientRecipes.objects.create(
            recipe=recipe,
            ingredient=ingredient,
            amount=ingredient_data.get('amount')
        )
