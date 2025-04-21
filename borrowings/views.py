from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowingCreateSerializer, BorrowingReturnSerializer
from telegram_notifications.message_builder import build_borrowing_created_message, build_borrowing_closed_message
from telegram_notifications.telegram import send_telegram_message


class BaseBorrowingView(generics.GenericAPIView):
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]
    queryset = Borrowing.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset


class BorrowingListView(BaseBorrowingView, generics.ListAPIView):
    pass


class BorrowingRetrieveView(BaseBorrowingView, generics.RetrieveAPIView):
    pass


class BorrowingCreateView(generics.CreateAPIView):
    serializer_class = BorrowingCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        borrowing = serializer.save(user=self.request.user)
        message = build_borrowing_created_message(borrowing)
        send_telegram_message(message)


class BorrowingReturnView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            borrowing = Borrowing.objects.get(pk=pk)
        except Borrowing.DoesNotExist:
            return Response(
                {"detail": "Borrowing not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not request.user.is_staff and borrowing.user != request.user:
            return Response(
                {"detail": "You do not have permission to return this borrowing."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = BorrowingReturnSerializer(
            instance=borrowing,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        if instance.actual_return_date:
            message = build_borrowing_closed_message(instance)
            send_telegram_message(message)

        return Response(
            {
                "detail": "Book returned successfully.",
                "borrowing": {
                    "id": borrowing.id,
                    "actual_return_date": borrowing.actual_return_date
                }
            },
            status=status.HTTP_200_OK
        )
