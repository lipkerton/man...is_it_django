from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from users.views import (
    CreateToken, DeleteToken, AvatarViewSet, CustomUserViewSet
)
from recipes.views import TagViewSet, IngredientViewSet, RecipeViewSet

router = SimpleRouter()

router.register(r'users', CustomUserViewSet, 'users')
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)

core_patterns = [
    path('', include(router.urls)),
    path('auth/token/login/', CreateToken.as_view()),
    path('auth/token/logout/', DeleteToken.as_view()),
    path('users/me/avatar/', AvatarViewSet.as_view(
        {'put': 'update', 'delete': 'destroy'})
    ),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(core_patterns)),
]
