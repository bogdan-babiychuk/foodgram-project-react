from rest_framework.pagination import PageNumberPagination

class RecipesPagination(PageNumberPagination):
    """Пагинация для рецептов"""
    page_size = 6
