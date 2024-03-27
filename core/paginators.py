from rest_framework import pagination


class BookPaginator(pagination.PageNumberPagination):
    page_size = 5
