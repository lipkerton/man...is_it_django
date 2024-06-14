from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    avatar = models.ImageField(upload_to='user_pics/', null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True, verbose_name='мыло')
    first_name = models.CharField(max_length=150, verbose_name='имя')
    last_name = models.CharField(max_length=150, verbose_name='фамилия')
    is_subscribed = models.BooleanField(default=False)
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
