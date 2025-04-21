from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowingCreateSerializer, BorrowingReturnSerializer


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
        serializer.save(user=self.request.user)
