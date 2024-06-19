from rest_framework import serializers

from users.fields import Base64ImageField
from users.serializers import CustomUserSerializer
from .methods import get_bool_cart_fav, validate_fav_cart
from .models import (Favorite, Ingredient, Recipe, RecipeIngredient, RecipeTag,
                     ShoppingCart, Tag)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientRepSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(
        source='ingredient.id'
    )
    name = serializers.CharField(
        source='ingredient.name'
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id', 'name', 'measurement_unit', 'amount'
        )


class RecipeTagRepSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(
        source='tag.id'
    )
    name = serializers.CharField(
        source='tag.name'
    )
    slug = serializers.SlugField(
        source='tag.slug'
    )

    class Meta:
        model = RecipeTag
        fields = (
            'id', 'name', 'slug'
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        required=True,
    )
    amount = serializers.IntegerField(
        min_value=1,
        required=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')

    def to_representation(self, instance):
        serializer = RecipeIngredientRepSerializer(
            instance=instance
        )
        return serializer.data


class RecipeTagField(serializers.PrimaryKeyRelatedField):

    def to_representation(self, instance):
        serializer = RecipeTagRepSerializer(
            instance=instance
        )
        return serializer.data


class RecipeCSerializer(serializers.ModelSerializer):

    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = RecipeIngredientSerializer(
        many=True,
        source='recipe_ingredient'
    )
    tags = RecipeTagField(
        queryset=Tag.objects.all(),
        many=True,
        source='recipe_tag'
    )
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author',
            'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name',
            'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, attrs):

        result = get_bool_cart_fav(
            cart_fav_obj=Favorite,
            data=self,
            attrs=attrs
        )

        if result:
            return True
        return result

    def get_is_in_shopping_cart(self, attrs):

        result = get_bool_cart_fav(
            cart_fav_obj=ShoppingCart,
            data=self,
            attrs=attrs
        )

        if result:
            return True
        return result

    def tag_ingredient_create(self, ingredients, tags, recipe):

        ingredients_obj = [
            RecipeIngredient(
                recipe=recipe,
                amount=ingredient.get('amount'),
                ingredient=ingredient.get('id'),
            ) for ingredient in ingredients
        ]
        tags_obj = [
            RecipeTag(
                recipe=recipe,
                tag=tag
            ) for tag in tags
        ]
        RecipeIngredient.objects.bulk_create(ingredients_obj)
        RecipeTag.objects.bulk_create(tags_obj)

    def create(self, validated_data, **kwargs):

        ingredients = validated_data.pop('recipe_ingredient')
        tags = validated_data.pop('recipe_tag')
        recipe = Recipe.objects.create(
            author=self.context.get('request').user,
            **validated_data
        )

        self.tag_ingredient_create(
            ingredients=ingredients,
            tags=tags,
            recipe=recipe
        )

        return recipe

    def update(self, instance, validated_data):

        ingredients = validated_data.pop('recipe_ingredient')
        tags = validated_data.pop('recipe_tag')

        instance.tags.clear()
        RecipeIngredient.objects.filter(recipe=instance).delete()

        self.tag_ingredient_create(
            ingredients=ingredients,
            tags=tags,
            recipe=instance
        )

        return super().update(instance, validated_data)

    def validate(self, attrs):

        ingredients = attrs.get('recipe_ingredient', None)
        tags = attrs.get('recipe_tag', None)
        cooking_time = attrs.get('cooking_time', None)

        if ingredients is None:
            raise serializers.ValidationError(
                'Поле для ингредиентов не было передано в сериализатор!'
            )

        ingredients = [
            ingredient['id'] for ingredient in ingredients
        ]

        if not ingredients:
            raise serializers.ValidationError(
                'Список ингредиентов пуст!'
            )

        if not tags:
            raise serializers.ValidationError(
                'Список тегов пуст!'
            )

        if cooking_time <= 0:
            raise serializers.ValidationError(
                'Указано неверное время приготовления!'
            )

        if len(ingredients) > len(set(ingredients)):
            raise serializers.ValidationError(
                'Имеются повторяющиеся ингредиенты!'
            )

        if len(tags) > len(set(tags)):
            raise serializers.ValidationError(
                'Имеются повторяющиеся ингредиенты!'
            )

        return super().validate(attrs)


class ShoppingCartSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(
        source='recipe.id',
        read_only=True
    )
    name = serializers.CharField(
        source='recipe.name',
        read_only=True
    )
    image = serializers.ImageField(
        source='recipe.image',
        read_only=True
    )
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time',
        read_only=True
    )

    class Meta:
        model = ShoppingCart
        fields = (
            'id', 'name', 'image', 'cooking_time'
        )

    def create(self, validated_data):

        user = self.context.get('request').user
        recipe = Recipe.objects.get(
            id=self.context.get('view').kwargs.get('pk')
        )

        shopping_cart = ShoppingCart.objects.create(
            user=user,
            recipe=recipe
        )

        return shopping_cart

    def validate(self, attrs):

        return validate_fav_cart(
            recipe_obj=Recipe,
            data=self,
            cart_fav_obj=ShoppingCart,
            place='корзине',
            attrs=attrs
        )


class FavoriteSerializer(ShoppingCartSerializer):

    def create(self, validated_data):

        user = self.context.get('request').user
        recipe = Recipe.objects.get(
            id=self.context.get('view').kwargs.get('pk')
        )

        favorites = Favorite.objects.create(
            user=user,
            recipe=recipe
        )

        return favorites

    def validate(self, attrs):

        return validate_fav_cart(
            recipe_obj=Recipe,
            data=self,
            cart_fav_obj=Favorite,
            place='избранном',
            attrs=attrs
        )
