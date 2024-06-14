import base64
from django.core.files.base import ContentFile
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers

from .models import User


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
