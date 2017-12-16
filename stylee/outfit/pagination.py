from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)

class OutfitLimitOffsetPagination(PageNumberPagination):
    page_size = 18
