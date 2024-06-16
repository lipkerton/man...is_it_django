import base64
from rest_framework import status
from rest_framework.response import Response
from django.core.files.base import ContentFile
from django.http import Http404
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers

from .models import User, Subscription
from recipes.models import Recipe


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):

        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class AvatarSerializer(serializers.ModelSerializer):

    avatar = Base64ImageField(required=True, allow_null=False)

    class Meta:
        model = User
        fields = ('avatar', )

    def update(self, instance, validated_data):

        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'id',
            'username', 'first_name',
            'last_name', 'password',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }


class CustomUserSerializer(UserSerializer):

    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'email', 'id',
            'username', 'first_name',
            'last_name', 'is_subscribed',
            'avatar'
        )


class SubscribeSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        source='subscriber.email',
        read_only=True
    )
    username = serializers.CharField(
        source='subscriber.username',
        read_only=True
    )
    first_name = serializers.CharField(
        source='subscriber.first_name',
        read_only=True
    )
    last_name = serializers.CharField(
        source='subscriber.last_name',
        read_only=True
    )
    avatar = serializers.ImageField(
        source='subscriber.avatar',
        read_only=True
    )
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:

        model = Subscription
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
            'is_subscribed', 'recipes',
            'recipes_count', 'avatar'
        )

    def get_recipes(self, attrs):

        recipes = Recipe.objects.filter(author=attrs.user)
        instance = [
            {
                'id': data.id,
                'name': data.name,
                'image': data.image.url,
                'cooking_time': data.cooking_time
            } for data in recipes
        ]

        return instance

    def get_recipes_count(self, attrs):
        return Recipe.objects.filter(author=attrs.user).count()

    def get_is_subscribed(self, attrs):
        return Subscription.objects.filter(user=attrs.user).exists()

    def create(self, validated_data):
        subscriber = self.context.get('request').user
        user = User.objects.get(
            id=self.context.get('view').kwargs.get('pk')
        )
        subscription = Subscription.objects.create(
            user=user,
            subscriber=subscriber
        )
        return subscription

    def validate(self, attrs):

        subscriber = self.context.get('request').user

        try:
            user = User.objects.get(
                id=self.context.get('view').kwargs.get('pk')
            )
        except User.DoesNotExist:
            raise Http404

        subscription = Subscription.objects.filter(
            user=user,
            subscriber=subscriber
        ).count()

        if subscriber == user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )

        if subscription > 0:
            raise serializers.ValidationError(
                'Такая подписка уже существует'
            )

        return super().validate(attrs)


class AuthTokenSerializer(serializers.Serializer):

    email = serializers.CharField(label="Email")
    password = serializers.CharField(
        label="Password", style={'input_type': 'password'}
    )

    def validate(self, attrs):

        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except Exception:
            raise serializers.ValidationError(
                'Такого юзера не существует!'
            )

        if email is None:
            raise serializers.ValidationError(
                'Мейл не заполнен!'
            )

        if password is None:
            raise serializers.ValidationError(
                'Пароль не заполнен!'
            )

        attrs['user'] = user
        return attrs
