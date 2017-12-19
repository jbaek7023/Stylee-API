from rest_framework.pagination import (
    PageNumberPagination,
)

class StarPagination(PageNumberPagination):
    page_size = 21
