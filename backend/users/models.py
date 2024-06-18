from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):

    avatar = models.ImageField(
        upload_to='user_pics/', null=True, blank=True
    )
    email = models.EmailField(
        max_length=254, unique=True, verbose_name='мыло'
    )
    first_name = models.CharField(
        max_length=150, verbose_name='имя'
    )
    last_name = models.CharField(
        max_length=150, verbose_name='фамилия'
    )
    is_subscribed = models.BooleanField(
        default=False, verbose_name='подписан'
    )
    recipes_count = models.IntegerField(
        default=0, verbose_name='количество рецептов'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='никнейм',
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z'
            ),
        ]
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'пользователи'


class Subscription(models.Model):

    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
        related_name='subscriber'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
        related_name='user'
    )

    class Meta:
        unique_together = ('subscriber', 'user')
