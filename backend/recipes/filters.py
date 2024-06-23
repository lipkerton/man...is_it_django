from django_filters import rest_framework

from .models import Favorite, Recipe, ShoppingCart, Ingredient, Tag


class RecipeFilter(rest_framework.FilterSet):

    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        conjoined=True,
        queryset=Tag.objects.all(),
    )
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    is_favorited = rest_framework.BooleanFilter(
        method='filter_is_favorite'
    )

    def filter_is_in_shopping_cart(self, queryset, name, value):

        if (
            self.request.user.is_authenticated
            and value
        ):
            shop_cart = ShoppingCart.objects.filter(
                user=self.request.user,
            ).values('recipe_id')
            return queryset.filter(id__in=shop_cart)
        return queryset

    def filter_is_favorite(self, queryset, name, value):

        if (
            self.request.user.is_authenticated
            and value
        ):
            fav = Favorite.objects.filter(
                user=self.request.user
            ).values('recipe_id')
            return queryset.filter(id__in=fav)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_in_shopping_cart', 'is_favorited')


class IngredientFilter(rest_framework.FilterSet):

    name = rest_framework.CharFilter(
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)
