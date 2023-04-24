from rest_framework import viewsets

from book.models import Book
from book.serializers import (
    BookSerializer,
    BookListSerializer,
    BookDetailSerializer,
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        if (
                self.action == "retrieve" or
                self.action == "partial_update" or
                self.action == "update"
        ):
            return BookDetailSerializer

        return BookSerializer
