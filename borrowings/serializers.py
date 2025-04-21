from rest_framework import serializers
from django.utils import timezone

from borrowings.models import Borrowing
from books.models import Book
from books.serializers import BookSerializer
from users.serializers import UserSerializer


class BorrowingSerializer(serializers.Serializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user"
        ]


class BorrowingCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Borrowing
        fields = [
            "book",
            "expected_return_date",
            "user"
        ]
        extra_kwargs = {
            "book": {"required": True},
            "expected_return_date": {"required": True},
        }

        def validate_book(self, book: Book):
            if book.inventory <= 0:
                raise serializers.ValidationError("This book is out of stock.")
            return book

        def validate(self, attrs):
            if attrs['expected_return_date'] <= timezone.now().date():
                raise serializers.ValidationError({
                    'expected_return_date': 'Return date must be in the future'
                })
            return attrs
