# from django_filters.rest_framework import FilterSet, filters 

# from rest_framework.filters import SearchFilter 

 

# from recipe.models import Ingredient, Recipes, Tag 

 

 

# class IngredientFilter(SearchFilter): 
#     search_param = 'name' 

#     class Meta:
#         model = Ingredient 
#         fields = ('name',) 


# class RecipeFilter(FilterSet):  
#     author = filters.CharFilter(field_name="author__id")  
#     tags = filters.ModelMultipleChoiceFilter(field_name='tags__slug', 
#                                              to_field_name='slug', 
#                                              queryset=Tag.objects.all(),) 

#     # def filter_is_favorited(self, queryset, name, value): 
#     #     client = self.request.user 
#     #     if value and client.is_authenticated: 
#     #         return queryset.filter(favorites__user=client) 
#     #     return queryset 

 
#     # def filter_is_in_shopping_cart(self, queryset, name, value): 
#     #     client = self.request.user 
#     #     if value and client.is_authenticated: 
#     #         return queryset.filter(shopping_cart__user=client) 
#     #     return queryset 


#     class Meta: 
#         model = Recipes
#         fields = ('author', 'tags') 
