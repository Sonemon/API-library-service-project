from datetime import date

from django.core.validators import MinValueValidator
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
    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.filter(inventory__gt=0),
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
            "expected_return_date": {
                "required": True,
                "validators": [MinValueValidator(date.today())]
            },
        }

        def validate_book(self, book: Book):
            if book.inventory < 1:
                raise serializers.ValidationError(
                    {
                        "book": f"Book {book.title} is out of stock",
                        "available": False,
                        "inventory": 0
                    }
                )
            return book

        def create(self, validated_data):
            book = validated_data["book"]
            user = validated_data["user"]
            expected_return_date = validated_data["expected_return_date"]

            return Borrowing.objects.create(
                book=book,
                user=user,
                expected_return_date=expected_return_date
            )
