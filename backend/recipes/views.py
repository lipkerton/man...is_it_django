from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from urlshortner.utils import shorten_url

from .filters import IngredientFilter, RecipeFilter
from .methods import get_shopping_cart_favorite_obj, random_naming_method
from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeCSerializer, RecipeIngredientSerializer,
                          ShoppingCartSerializer, TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.all()
    serializer_class = RecipeCSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_link(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        main_part = request._request._current_scheme_host
        new_link = f'recipes/{pk}'
        mini_link = shorten_url(
            f'{main_part}/{new_link}',
            is_permanent=False
        )
        return Response(
            {'short-link': f'{main_part}/s/{mini_link}'}
        )


class ShopCartViewSet(viewsets.ModelViewSet):

    queryset = ShoppingCart
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return get_shopping_cart_favorite_obj(
            recipe_obj=Recipe,
            data=self,
            shopping_cart_favorite_obj=ShoppingCart,
            place='корзина'
        )

    def download(self, request):
        shopping_cart = ShoppingCart.objects.filter(
            user=request.user
        )
        file_name = random_naming_method()
        messages = []
        for pack in shopping_cart:
            recipe_ingredient = RecipeIngredient.objects.filter(
                recipe_id=pack.recipe.id
            )
            serializer = RecipeIngredientSerializer(
                recipe_ingredient, many=True
            )
            ingredients = []
            for ingredient in serializer.data:
                name = ingredient.get('name')
                measurement_unit = ingredient.get('measurement_unit')
                amount = ingredient.get('amount')
                ingredient_message = (
                    f'  Ингредиент - {name} \n'
                    f'  Мера измерения - {measurement_unit} \n'
                    f'  Количество - {amount} \n'
                )
                ingredients.append(ingredient_message)
            ingredients_content = '\n'.join(ingredients)
            message = (
                f'Ваша покупка - {pack.recipe.name},\n'
                f'Ингредиенты:\n'
                f'{ingredients_content}\n'
                f'Время приготовления - {pack.recipe.cooking_time}.'
                '\n'
            )
            messages.append(message)
        response_content = '\n'.join(messages)
        response = HttpResponse(
            response_content, content_type='text/plain,charset=utf8'
        )
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        return response


class FavoriteViewSet(viewsets.ModelViewSet):

    queryset = Favorite
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthorOrReadOnly, )

    def get_object(self):
        return get_shopping_cart_favorite_obj(
            recipe_obj=Recipe,
            data=self,
            shopping_cart_favorite_obj=Favorite,
            place='избранное'
        )
