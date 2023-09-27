from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .views import IngredientViewSet, TagViewSet, RecipesViewSet
from users.views import CustomUserViewSet
app_name = 'api'

router = DefaultRouter()

router.register('users', CustomUserViewSet)
router.register('tags', TagViewSet),
router.register('ingredients', IngredientViewSet),
router.register('recipes', RecipesViewSet)


urlpatterns = [
    # Все зарегистрированные в router пути доступны в router.urls
    # Включим их в головной urls.py
    path('', include(router.urls)),
    path('', include("djoser.urls")),
    re_path(r'auth/', include('djoser.urls.authtoken')),
]
