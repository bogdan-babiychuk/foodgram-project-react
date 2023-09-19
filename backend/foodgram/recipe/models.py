from django.db import models
from users.models import User

from django.db import models
from colorfield.fields import ColorField
from django.core.validators import MinValueValidator

# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=256)
    color = ColorField()
    slug = models.SlugField(unique=True, max_length=255)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
    
    def __str__(self) -> str:
        return self.title
    
class Ingredient(models.Model):
    name = models.CharField(max_length=256)

    units = models.CharField(max_length=60, default='г')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return self.name
    

class Recipes(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор')
    
    title = models.CharField(max_length=256, verbose_name="Название рецепта")
    image = models.ImageField(upload_to= 'recipts/')

    description = models.TextField(blank=True,
                                   verbose_name="Описание рецепта")
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientRecipes',
                                         blank=True,
                                         verbose_name='Ингредиенты')
    tags = models.ManyToManyField(Tag, related_name='recipes')

    cooking_time = models.IntegerField(validators=[MinValueValidator(1)],
                                       default=1,
                                       verbose_name="Время приготовления")

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title

class IngredientRecipes(models.Model):
    recipe = models.ForeignKey(Recipes,
                               on_delete=models.CASCADE,
                               related_name='ingredients_used')
    
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name= 'recipe',
                                   verbose_name='Ингредиенты')
    
    quantity = models.DecimalField(max_digits=10,
                                   decimal_places=2,
                                   default=0.5,
                                   verbose_name='Количество')
    
    units = models.CharField(max_length=100, verbose_name='Единицы измерения')
    
    
    def __str__(self):
        return f'{self.recipe} {self.ingredient}'
