from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (AvatarViewSet, CreateToken, CustomUserViewSet, DeleteToken,
                    SubscriptionViewSet)

router = SimpleRouter()

router.register(r'users', CustomUserViewSet, 'users')

urlpatterns = [
    path('auth/token/login/', CreateToken.as_view(), name='login'),
    path('auth/token/logout/', DeleteToken.as_view(), name='logout'),
    path('users/me/avatar/', AvatarViewSet.as_view(
        {'put': 'update', 'delete': 'destroy'}
    ), name='avatar'),
    path('users/<int:pk>/subscribe/', SubscriptionViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'}
    ), name='subscribe'),
    path('users/subscriptions/', SubscriptionViewSet.as_view(
        {'get': 'list'}
    ), name='subscriptions'),
    path('', include(router.urls)),
]
