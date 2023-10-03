from django.contrib import admin
from django.template.loader import get_template
from .models import Tag, Recipes, Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'units')
    list_filter = ('name', )


class IngredientRecipesInline(admin.TabularInline):
    model = Recipes.ingredients.through
    extra = 1


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    inlines = (IngredientRecipesInline,)
    list_display = ('id', 'author', 'name')
    list_display_links = ('name',)
    fields = ('author', 'name', 'tags', 'ingredient',
              'text', 'cooking_time', 'image')
    list_filter = ('author', 'name', 'tags')
    readonly_fields = ('ingredient',)

    def ingredient(self, *args, **kwargs):
        context = getattr(self.response, 'context_data', None) or {}
        inline = context['inline_admin_formset'] = context[
                        'inline_admin_formsets'].pop(0)
        return get_template(inline.opts.template).render(context, self.request)

    def render_change_form(self, request, *args, **kwargs):
        self.request = request
        self.response = super().render_change_form(request, *args, **kwargs)
        return self.response

    # def get_tags(self, obj):
    #     return ', '.join(tag.title for tag in Teg.objects.all())
    # get_tags.short_description = 'Теги'


admin.site.site_title = 'Administration Foodgram'
admin.site.site_header = 'Foodgram Admin Panel'
admin.site.register(Tag)
