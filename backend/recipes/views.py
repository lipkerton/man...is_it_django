from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.http import Http404

from .models import (
    Tag, Ingredient, Recipe, ShoppingCart, Favorite,
)
from users.models import User
from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeCSerializer,
    ShoppingCartSerializer,
    FavoriteSerializer
)
from .permissions import IsAuthorOrReadOnly


class TagViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.all()
    serializer_class = RecipeCSerializer
    permission_classes = (IsAuthorOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )


class ShopCartViewSet(viewsets.ModelViewSet):

    queryset = ShoppingCart
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        user = self.request.user

        try:
            recipe = Recipe.objects.get(
                id=self.kwargs.get('pk')
            )
        except Recipe.DoesNotExist:
            raise Http404

        try:
            shopping_cart = ShoppingCart.objects.get(
                user=user,
                recipe=recipe
            )
        except ShoppingCart.DoesNotExist:
            raise ValidationError(
                'Такого товара в корзине нет!'
            )

        return shopping_cart


class FavoriteViewSet(viewsets.ModelViewSet):

    queryset = Favorite
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        user = self.request.user

        try:
            recipe = Recipe.objects.get(
                id=self.kwargs.get('pk')
            )
        except Recipe.DoesNotExist:
            raise Http404

        try:
            shopping_cart = Favorite.objects.get(
                user=user,
                recipe=recipe
            )
        except Favorite.DoesNotExist:
            raise ValidationError(
                'Такого товара в избранном нет!'
            )

        return shopping_cart
