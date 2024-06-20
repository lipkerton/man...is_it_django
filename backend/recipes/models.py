from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


class Tag(models.Model):

    name = models.CharField(max_length=254, verbose_name='Имя тега')
    slug = models.SlugField(
        unique=True,
        max_length=32,
        verbose_name='slug',
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$'
            ),
        ]
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'теги'


class Ingredient(models.Model):

    name = models.CharField(
        max_length=254,
        verbose_name='Имя ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=10,
        verbose_name='Мера измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'ингредиенты'


class ShoppingCart(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Юзер'
    )
    recipe = models.ForeignKey(
        to='Recipe',
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique recipe_user_shopping_cart'
            )
        ]


class Favorite(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Юзер'
    )
    recipe = models.ForeignKey(
        to='Recipe',
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique recipe_user_favorite'
            )
        ]


class RecipeIngredient(models.Model):

    recipe = models.ForeignKey(
        to='Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField()

    class Meta:
        default_related_name = 'recipe_ingredient'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique recipe_ingredient'
            )
        ]


class RecipeTag(models.Model):

    recipe = models.ForeignKey(to='Recipe', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'recipe_tag'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='unique recipe_tag'
            )
        ]


class Recipe(models.Model):

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        through_fields=('recipe', 'tag'),
        verbose_name='Теги'
    )
    image = models.ImageField(
        upload_to='recipe_pics/',
        verbose_name='картинка'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Наименование'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.SmallIntegerField(
        verbose_name='Время готовки'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'рецепты'
