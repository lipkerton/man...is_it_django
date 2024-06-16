from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from users.views import (
    CreateToken,
    DeleteToken,
    AvatarViewSet,
    CustomUserViewSet,
    SubscriptionViewSet
)
from recipes.views import (
    TagViewSet,
    IngredientViewSet,
    RecipeViewSet,
    ShopCartViewSet,
    FavoriteViewSet
)

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
    path('recipes/<int:pk>/favorite/', FavoriteViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'}
    )),
    path('', include(router.urls)),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(core_patterns)),
]
