from rest_framework.routers import SimpleRouter
from django.urls import include, path

from recipes.views import (
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
    ShopCartViewSet,
    FavoriteViewSet
)

router = SimpleRouter()

router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('recipes/<int:pk>/get-link/', RecipeViewSet.as_view(
        {'get': 'get_link'}
    )),
    path('recipes/<int:pk>/shopping_cart/', ShopCartViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'}
    )),
    path('recipes/download_shopping_cart/', ShopCartViewSet.as_view(
        {'get': 'download'}
    )),
    path('recipes/<int:pk>/favorite/', FavoriteViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'}
    )),
    path('s/', include("urlshortner.urls")),
    path('', include(router.urls)),
]
