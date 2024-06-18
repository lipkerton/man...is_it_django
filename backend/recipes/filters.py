from django_filters import FilterSet, CharFilter, BooleanFilter, ModelChoiceFilter

from .models import Recipe
from users.models import User


class RecipeFilter(FilterSet):

    tags = CharFilter(
        field_name="tags__name", method='filter_tags'
    )
    is_favorited = BooleanFilter()
    is_in_shopping_cart = BooleanFilter()
    author = ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Recipe
        fields = ('tags', 'is_favorited', 'is_in_shopping_cart', 'author')

    def filter_tags(self, queryset, name, tags):
        return queryset.filter(tags__name__contains=tags.split(','))
