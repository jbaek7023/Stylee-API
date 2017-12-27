from rest_framework.pagination import (
    PageNumberPagination,
)

class FollowPagination(PageNumberPagination):
    page_size = 30
