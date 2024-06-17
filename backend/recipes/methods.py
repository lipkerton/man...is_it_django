import random

from django.http import Http404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


def get_cart_fav(ype, data, add_ype, place):

    user = data.request.user

    try:
        recipe = ype.objects.get(
            id=data.kwargs.get('pk')
        )
    except ype.DoesNotExist:
        raise Http404

    try:
        obj = add_ype.objects.get(
            user=user,
            recipe=recipe
        )
    except add_ype.DoesNotExist:
        raise ValidationError(
            f'Такого товара в {place} нет!'
        )

    return obj


def validate_fav_cart(ype, data, add_ype, place, attrs):

    user = data.context.get('request').user

    try:
        recipe = ype.objects.get(
            id=data.context.get('view').kwargs.get('pk')
        )
    except ype.DoesNotExist:
        raise serializers.ValidationError(
            'Такого рецепта не существует!'
        )

    obj_counter = add_ype.objects.filter(
        user=user,
        recipe=recipe
    ).count()

    if obj_counter > 0:
        raise serializers.ValidationError(
            f'Этот рецепт уже в {place}!'
        )

    return attrs


def get_bool_cart_fav(ype, data, attrs):

    user = data.context.get('request').user

    try:
        obj = ype.objects.get(
            user=user,
            recipe=attrs
        )
    except ype.DoesNotExist:
        return False

    except TypeError:
        return False

    return obj.recipe


def random_naming_method():
    return ''.join(
        [
            random.choice(
                list(
                    '123456789qwertyuiopasdfghjklzx',
                    'cvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
                )
            ) for x in range(12)
        ]
    )
