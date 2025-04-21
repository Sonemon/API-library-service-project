from django.utils import timezone

from rest_framework import serializers

from borrowings.models import Borrowing
from books.models import Book
from books.serializers import BookSerializer
from telegram_notifications.message_builder import build_borrowing_created_message
from telegram_notifications.telegram import send_telegram_message
from users.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
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
            "id",
            "book",
            "expected_return_date",
            "user"
        ]

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

        def validate_expected_return_date(self, value):
            if value < timezone.localdate():
                raise serializers.ValidationError("Expected return date must be in the future.")
            return value

        def create(self, validated_data):
            borrowing = Borrowing.objects.create(**validated_data)

            message = build_borrowing_created_message(borrowing)
            send_telegram_message(message)

            return borrowing


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ["id"]

    def update(self, instance, validated_data):
        instance.return_borrowing()
        return instance
