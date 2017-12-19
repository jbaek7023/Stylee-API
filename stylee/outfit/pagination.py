from rest_framework.pagination import (
    PageNumberPagination,
)

class OutfitPagination(PageNumberPagination):
    page_size = 24

class CategoryPagination(PageNumberPagination):
    page_size = 12
