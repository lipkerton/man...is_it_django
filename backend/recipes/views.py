from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from urlshortner.utils import shorten_url

from .methods import get_cart_fav, random_naming_method
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .permissions import IsAuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeCSerializer, ShoppingCartSerializer,
                          TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.all()
    serializer_class = RecipeCSerializer
    permission_classes = (IsAuthorOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'is_favorited',
        'author',
        'is_in_shopping_cart',
        'tags'
    )

    def get_link(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        main_part = 'http://localhost:8000/recipes/'
        mini_link = shorten_url(
            f'{main_part}{pk}',
            is_permanent=False
        )
        return Response(
            {'short-link': f'{main_part}s/{mini_link}'}
        )


class ShopCartViewSet(viewsets.ModelViewSet):

    queryset = ShoppingCart
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return get_cart_fav(
            ype=Recipe,
            data=self,
            add_ype=ShoppingCart,
            place='корзина'
        )

    def download(self, request, name):

        return FileResponse(f'./files/{name}', as_attachment=True)

    def write_file_name(self, request):
        package = ShoppingCart.objects.filter(
            user=request.user
        )
        rnd_file_name = random_naming_method()
        with open(f'./files{rnd_file_name}', 'w') as dwnl:
            for pack in package:
                dwnl.write(
                    f'Ваша покупка - {pack.name}, ',
                    f'Время приготовления - {pack.cooking_time}.'
                    '\n'
                )
        return self.download(name=rnd_file_name)


class FavoriteViewSet(viewsets.ModelViewSet):

    queryset = Favorite
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return get_cart_fav(
            ype=Recipe,
            data=self,
            add_ype=Favorite,
            place='избранное'
        )
