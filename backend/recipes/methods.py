import random
import string

from django.http import Http404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


def get_cart_fav(recipe_obj, data, cart_fav_obj, place):

    user = data.request.user

    try:
        recipe = recipe_obj.objects.get(
            id=data.kwargs.get('pk')
        )
    except recipe_obj.DoesNotExist:
        raise Http404

    try:
        obj = cart_fav_obj.objects.get(
            user=user,
            recipe=recipe
        )
    except cart_fav_obj.DoesNotExist:
        raise ValidationError(
            f'Такого товара в {place} нет!'
        )

    return obj


def validate_fav_cart(recipe_obj, data, cart_fav_obj, place, attrs):

    user = data.context.get('request').user

    try:
        recipe = recipe_obj.objects.get(
            id=data.context.get('view').kwargs.get('pk')
        )
    except recipe_obj.DoesNotExist:
        raise serializers.ValidationError(
            'Такого рецепта не существует!'
        )

    obj_existence = cart_fav_obj.objects.filter(
        user=user,
        recipe=recipe
    ).exists()

    if obj_existence:
        raise serializers.ValidationError(
            f'Этот рецепт уже в {place}!'
        )

    return attrs


def get_bool_cart_fav(cart_fav_obj, data, attrs):

    user = data.context.get('request').user

    try:
        obj = cart_fav_obj.objects.get(
            user=user,
            recipe=attrs
        )
    except cart_fav_obj.DoesNotExist:
        return False

    except TypeError:
        return False

    return obj.recipe


def random_naming_method():
    numbers_letters = string.ascii_letters + string.digits
    return ''.join(
        [
            random.choice(
                list(
                    numbers_letters
                )
            ) for x in range(12)
        ]
    )
