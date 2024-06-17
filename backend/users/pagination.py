from rest_framework.pagination import LimitOffsetPagination


class CustomPagination(LimitOffsetPagination):

    limit_query_param = 'recipe_limit'
