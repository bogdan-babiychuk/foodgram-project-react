from django.db import models
from users.models import User
from django.db.models import (
    Q,
    F,
    UniqueConstraint,
    CheckConstraint
)
from colorfield.fields import ColorField
from django.core.validators import MinValueValidator


class Tag(models.Model):
    name = models.CharField(max_length=256)
    color = ColorField()
    slug = models.SlugField(unique=True, max_length=255)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    units = models.CharField(max_length=60, default='г')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор'
    )

    name = models.CharField(max_length=256, verbose_name="Название рецепта")
    image = models.ImageField(upload_to='media/images')

    text = models.TextField(
        blank=True,
        verbose_name="Описание рецепта"
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(Tag, related_name='recipes')

    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)],
        default=1,
        verbose_name="Время приготовления"
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientRecipes(models.Model):
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='ingredients_used',
        null=True
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Ингредиенты'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.5,
        verbose_name='Количество',
        null=True
    )

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


class Follow(models.Model):
    """
    Подписки на авторов рецептов.
    """
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='follower',
        on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        User,
        verbose_name='Подписка',
        related_name='followed',
        on_delete=models.CASCADE
    )

    class Meta:
        """
        Пользователь может только 1 раз подписаться на автора.
        Нельзя подписаться на самого себя, оператор F достаёт текущю
        запись поля author.
        """
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='Уникальная подписка'
            ),
            CheckConstraint(
                check=~Q(user=F('author')),
                name='Запрет самоподписки'
            )
        ]


class Favorite(models.Model):
    """
    Любимые рецепты пользователя
    """
    user = models.ForeignKey(
        User,
        related_name='favorite',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )

    recipe = models.ForeignKey(
        Recipes,
        related_name='favorite',
        on_delete=models.CASCADE,
        verbose_name='Рецепты'
    )

    class Meta:
        """
        Нельзя добавлять в любимые один и тот же рецепт несколько раз
        """
        verbose_name = 'Любимые рецепты'
        verbose_name_plural = 'Любимые рецепты'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='Уникальность любимых рецептов'
            )
        ]

    def __str__(self):
        return f'{self.recipe}'


class List_Of_Purchases(models.Model):
    """Модель списка покупок"""
    user = models.ForeignKey(
        User,
        related_name='purchases',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    recipe = models.ForeignKey(
        Recipes,
        related_name='purchases',
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Список покупок'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='уникальные покупки'
            )
        ]

    def __str__(self):
        return f'{self.recipe}'
