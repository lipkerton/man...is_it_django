from rest_framework import serializers

from .models import Tag, Ingredient, RecipeIngredient, RecipeTag, Recipe
from users.serializers import CustomUserSerializer, Base64ImageField


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


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
        return {
            "id": instance.ingredient.id,
            "name": instance.ingredient.name,
            "measurement_unit": instance.ingredient.measurement_unit,
            "amount": instance.amount
        }


class RecipeTagField(serializers.PrimaryKeyRelatedField):

    def to_representation(self, instance):
        return {
            'id': instance.tag.id,
            'name': instance.tag.name,
            'slug': instance.tag.slug
        }


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
    is_favorited = serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author',
            'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name',
            'image', 'text', 'cooking_time'
        )

    def tag_ingredient_create(self, ingredients, tags, recipe):

        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                amount=ingredient.get('amount'),
                ingredient=ingredient.get('id'),
            )

        for tag in tags:
            RecipeTag.objects.create(
                recipe=recipe,
                tag=tag
            )

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
