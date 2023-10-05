from recipe.models import (
    ListOfPurchases,
    IngredientRecipes,
    Ingredient,
    Favorite,
    Recipes,
    Tag,
)

from .serializers import (
    IngredientSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    TagSerializer,
)

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .paginations import RecipesPagination
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from api.permissions import IsAuthorOrAdminOrReadOnly
from .filters import RecipeFilter, IngredientFilter
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.db.models import Sum
from django.http import HttpResponse
from datetime import datetime
from users.serializers import FavoriteFollowSerializer


class IngredientViewSet(ListModelMixin, RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter,)
    search_fields = ("^name",)
    pagination_class = None


class TagViewSet(ListModelMixin, RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    pagination_class = RecipesPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @action(detail=True, methods=["post", "delete"])
    def favorite(self, request, pk):
        """Добавление/удаление из избранного.
        Находим в базе рецепт, пытаемся создать пару
        рецепта и пользователя, если прошло всю проверку,
        то возвращаем данные с помощью Вспомогательного сериализатора
        FavoriteFollowSerializer
        В удаление, если есть пара юзера и рецепта, то только в таком
        случае можно убрать из избранного.
        """
        if not request.user.is_authenticated:
            return Response(
                {"favorites": "Нужно войти либо создать аккаунт"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        recipe = get_object_or_404(Recipes, id=pk)
        _, created = Favorite.objects.get_or_create(user=request.user,
                                                    recipe=recipe)

        if request.method == "POST":
            if not created:
                return Response(
                    {"favorites": "Рецепт уже добавлен в избранное"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = FavoriteFollowSerializer(
                recipe, context={'request': request})

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            recipe = Favorite.objects.filter(user=request.user, recipe__id=pk)
            if recipe.exists():
                recipe.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {"favorites": "Добавьте рецепт в избранное"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["post", "delete"])
    def shopping_cart(self, request, pk):
        """Та же логика работы, что и при добавлении в избранное"""
        if not request.user.is_authenticated:
            return Response(
                {"shopping_cart": "Требуется аутентификация"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        recipe = get_object_or_404(Recipes, id=pk)
        _, created = ListOfPurchases.objects.get_or_create(
            user=request.user, recipe=recipe)

        if request.method == "POST":
            if not created:
                return Response(
                    {"shopping_cart": "Рецепт уже добавлен в корзину"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = FavoriteFollowSerializer(
                recipe, context={'request': request})

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            cart_object = ListOfPurchases.objects.filter(user=request.user,
                                                         recipe__id=pk)
            if cart_object.exists():
                cart_object.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {"shopping_cart": "Рецепт не найден в корзине"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = (
            IngredientRecipes.objects
            .filter(recipe__purchases__user=request.user)
            .values("ingredient__name", "ingredient__units")
            .annotate(amount=Sum("amount"))
        )

        today = datetime.today()
        purchases_info = [
            f'- {ingredient["ingredient__name"]} - {ingredient["amount"]} '
            f'{ingredient["ingredient__units"]}'
            for ingredient in ingredients
        ]

        user_info = (
            f'Пользователь: {request.user.username} ({request.user.email})'
        )
        date_info = f"Дата: {today:%Y-%m-%d}"
        purchases_text = "\n".join([user_info, date_info] + purchases_info)

        filename = f"{request.user}_purchases.txt"
        response = HttpResponse(purchases_text, content_type="text/plain")
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response

    @action(detail=False, permission_classes=[IsAuthenticated])
    def get(self, request):
        return self.download_shopping_cart(request)
