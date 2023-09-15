from recipe .models import Ingredient, IngredientRecipes, Recipes, Tag
from rest_framework import serializers

class IngredientSerializer(serializers.ModelSerializer):
    """
    Базовый Сериализатор для ингредиентов 
    http://127.0.0.1:8000/api/v1/ingredients/
    
    """
    class Meta:
        model = Ingredient
        fields = '__all__'

class IngredientAddInRecipeSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(
        queryset= Ingredient.objects.all())
    
    class Meta:
        model = IngredientRecipes
        fields = ('id', 'quantity', )

class TagSerializer(serializers.ModelSerializer):
    """
    Базовый Сериализатор для тегов.
    http://127.0.0.1:8000/api/v1/tags/

    """
    class Meta:
        model = Tag
        fields = ('title', 'color', 'slug')

        
class IngredientRecipesSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вспомогательной модели IngredientRecipes
    благодаря source, можно получить ПРАВИЛЬНОE ID ингредиента
    и также строковое представление для название ингредиента
     
    """
    id = serializers.PrimaryKeyRelatedField(
        queryset = Ingredient.objects.all(), source='ingredient.id'
    ) 

    ingredient = serializers.PrimaryKeyRelatedField(
        queryset= Ingredient.objects.all(), source='ingredient.name'
    )

    class Meta:
        model = IngredientRecipes
        fields = ('id', 'ingredient', 'quantity', 'units')

class RecipeReadSerializer(serializers.ModelSerializer):
    """
    GET запрос для получения объектов модели Recipes
    http://127.0.0.1:8000/api/v1/recipes/

    """
    ingredients = IngredientRecipesSerializer(many=True,
                                              source='ingredients_used')
    tags = TagSerializer(read_only=True,
                        many=True)

    class Meta:
        model = Recipes
        fields = ('id', 'author', 'title', 'image', 'description', 'ingredients', 'tags', 'cooking_time')


class RecipeWriteSerializer(serializers.ModelSerializer):
    ingredients = IngredientAddInRecipeSerializer(many=True, write_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Recipes
        fields = ('id', 'author', 'title', 'description', 'ingredients', 'tags', 'cooking_time')

    
    def create(self, validated_data):
        tag_titles = validated_data.pop('tags', [])
        ingredient_data = validated_data.pop('ingredients', [])

        recipe = Recipes.objects.create(**validated_data)


        for ingredient in ingredient_data:
            ingredient_name = ingredient.get('ingredient')
            quantity = ingredient.get('quantity')

            # Создаем или получаем объект ингредиента
            ingredient_obj, created = Ingredient.objects.get(name=ingredient_name)

            # Создаем связь между рецептом и ингредиентом
            IngredientRecipes.objects.create(
                recipe=recipe,
                ingredient=ingredient_obj,
                quantity=quantity,
            )
            recipe.tags.set(tag_titles)

        return recipe
