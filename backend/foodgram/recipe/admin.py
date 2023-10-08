from django.contrib import admin
from django.template.loader import get_template
from .models import Tag, Recipes, Ingredient, Follow, Favorite, ListOfPurchases
from django import forms
from django.forms import BaseInlineFormSet


class IngredientFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        has_ingredients = False
        ingredients_set = set()
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('ingredient'):
                    has_ingredients = True
                    ingredient_id = form.cleaned_data['ingredient'].id
                    if ingredient_id in ingredients_set:
                        raise forms.ValidationError(
                              'Ингредиенты не могут повторяться.')
                    ingredients_set.add(ingredient_id)
        if not has_ingredients:
            raise forms.ValidationError(
                  'Рецепт должен содержать хотя бы один ингредиент.')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'units')
    list_filter = ('name', )


class IngredientRecipesInline(admin.TabularInline):
    model = Recipes.ingredients.through
    extra = 1
    formset = IngredientFormSet


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    inlines = (IngredientRecipesInline,)
    list_display = ('id', 'author', 'name', 'favorites_count')
    list_display_links = ('name',)
    fields = ('author', 'name', 'tags', 'ingredient',
              'text', 'cooking_time', 'image')
    list_filter = ('author', 'name', 'tags')
    readonly_fields = ('ingredient',)

    def favorites_count(self, obj):
        return obj.favorite.count()

    def ingredient(self, *args, **kwargs):
        context = getattr(self.response, 'context_data', None) or {}
        inline_admin_formsets = context['inline_admin_formsets']
        inline = context['inline_admin_formset'] = inline_admin_formsets.pop(0)
        return get_template(inline.opts.template).render(context, self.request)

    def render_change_form(self, request, *args, **kwargs):
        self.request = request
        self.response = super().render_change_form(request, *args, **kwargs)
        return self.response


admin.site.site_title = 'Administration Foodgram'
admin.site.site_header = 'Foodgram Admin Panel'
admin.site.register(Tag)
admin.site.register(ListOfPurchases)
admin.site.register(Favorite)
admin.site.register(Follow)
