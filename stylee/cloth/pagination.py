from rest_framework.pagination import (
    PageNumberPagination,
)

class ClothPagination(PageNumberPagination):
    page_size = 21
