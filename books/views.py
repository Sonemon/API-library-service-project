from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from books.models import Book
from books.permissions import IsAdminOrReadOnly
from books.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

    @extend_schema(
        description="List all available books (inventory > 0).",
        responses={status.HTTP_200_OK: BookSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def available(self, request):
        """List all available books."""
        available_books = self.get_queryset().filter(inventory__gt=0)
        serializer = self.get_serializer(available_books, many=True)
        return Response(serializer.data)
