from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.views import (AvatarViewSet, CreateToken, CustomUserViewSet,
                         DeleteToken, SubscriptionViewSet)
from recipes.views import (FavoriteViewSet, IngredientViewSet, RecipeViewSet,
                           ShopCartViewSet, TagViewSet)

router = SimpleRouter()

router.register(r'users', CustomUserViewSet, 'users')
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)

core_patterns = [
    path('auth/token/login/', CreateToken.as_view()),
    path('auth/token/logout/', DeleteToken.as_view()),
    path('users/me/avatar/', AvatarViewSet.as_view(
        {'put': 'update', 'delete': 'destroy'}
    )),
    path('users/<int:pk>/subscribe/', SubscriptionViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'}
    )),
    path('users/subscriptions/', SubscriptionViewSet.as_view(
        {'get': 'list'}
    )),
    path('recipes/<int:pk>/shopping_cart/', ShopCartViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'}
    )),
    path('recipes/download_shopping_cart', ShopCartViewSet.as_view(
        {'get': 'write_file_name'}
    )),
    path('recipes/<int:pk>/favorite/', FavoriteViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'}
    )),
    path('recipes/<int:pk>/get-link/', RecipeViewSet.as_view(
        {'get': 'get_link'}
    )),
    path('s/', include("urlshortner.urls")),
    path('', include(router.urls)),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(core_patterns)),
]
