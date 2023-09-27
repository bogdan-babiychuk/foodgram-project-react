from rest_framework import serializers
from recipe.models import IngredientRecipes, Ingredient
from django.shortcuts import get_object_or_404

class BaseRecipeSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для моделей Favorite и List_Of_Purchases."""

    id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='recipes.id',)
    title = serializers.ReadOnlyField(
        read_only=True,
        source='recipes.title',)
    image = serializers.ImageField(
        read_only=True,
        source='recipes.image',)
    coocking_time = serializers.IntegerField(
        read_only=True,
        source='recipe.cooking_time',)
    
    class Meta:
        abstract = True  # Делаем этот класс абстрактным


def create_ingredients(ingredients, recipe):
    """Вспомогательная функция для добавления ингредиентов.
    Используется при создании/редактировании рецепта."""
    ingredient_list = []
    for ingredient in ingredients:
        current_ingredient = get_object_or_404(Ingredient,
                                               id=ingredient.get('id'))
        quantity = ingredient.get('quantity')
        ingredient_list.append(
            IngredientRecipes(
                recipe=recipe,
                ingredient=current_ingredient,
                quantity=quantity
            )
        )
    IngredientRecipes.objects.bulk_create(ingredient_list)
        