from django.db import models
from django.core.validators import RegexValidator

from users.models import User


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
        max_length=254, verbose_name='Имя ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=10, verbose_name='Мера измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'ингредиенты'


class RecipeIngredient(models.Model):

    recipe = models.ForeignKey(to='Recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()

    class Meta:
        default_related_name = 'recipe_ingredient'


class RecipeTag(models.Model):

    recipe = models.ForeignKey(to='Recipe', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'recipe_tag'


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient')
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        through_fields=('recipe', 'tag')
    )
    image = models.ImageField()
    name = models.CharField(max_length=255)
    text = models.TextField()
    cooking_time = models.SmallIntegerField()
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)
