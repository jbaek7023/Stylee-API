from rest_framework.pagination import (
    PageNumberPagination,
)

class CategoryPagination(PageNumberPagination):
    page_size = 10
