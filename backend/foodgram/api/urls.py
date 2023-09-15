from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import IngredientViewSet, TagViewSet, RecipesViewSet

router = DefaultRouter()

router.register('tags', TagViewSet),
router.register('ingredients', IngredientViewSet),
router.register('recipes', RecipesViewSet)


urlpatterns = [
    # Все зарегистрированные в router пути доступны в router.urls
    # Включим их в головной urls.py
    path('v1/', include(router.urls)),
] 
