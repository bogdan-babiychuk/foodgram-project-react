from django.urls import include, path, re_path
from rest_framework import routers
from .views import IngredientViewSet, TagViewSet, RecipesViewSet
from users.views import CustomUserViewSet
app_name = 'api'

router = routers.DefaultRouter()

router.register('users', CustomUserViewSet, basename='users')
router.register('tags', TagViewSet),
router.register('ingredients', IngredientViewSet),
router.register('recipes', RecipesViewSet, basename='recipes')


urlpatterns = [
    path('', include(router.urls)),
    path('', include("djoser.urls")),
    re_path(r'auth/', include('djoser.urls.authtoken')),
]
