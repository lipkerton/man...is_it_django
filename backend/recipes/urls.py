from django.urls import include, path
from rest_framework.routers import SimpleRouter

from recipes.views import (FavoriteViewSet, IngredientViewSet, RecipeViewSet,
                           ShopCartViewSet, TagViewSet)

router = SimpleRouter()

router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('recipes/<int:pk>/get-link/', RecipeViewSet.as_view(
        {'get': 'get_link'}
    ), name='get_link'),
    path('recipes/<int:pk>/edit/', RecipeViewSet.as_view(
        {'patch': 'update'}
    ), name='update_recipe'),
    path('recipes/<int:pk>/shopping_cart/', ShopCartViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'}
    ), name='shopping_cart'),
    path('recipes/download_shopping_cart/', ShopCartViewSet.as_view(
        {'get': 'download'}
    ), name='download_shopping_cart'),
    path('recipes/<int:pk>/favorite/', FavoriteViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'}
    ), name='favorite'),
    path('s/', include("urlshortner.urls")),
    path('', include(router.urls)),
]
