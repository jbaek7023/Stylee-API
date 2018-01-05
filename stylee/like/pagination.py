from rest_framework.pagination import (
    PageNumberPagination,
)

class LikePagination(PageNumberPagination):
    page_size = 24
