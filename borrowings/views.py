from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer


class BorrowingListRetrieveView(generics.ListAPIView, generics.RetrieveAPIView):
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]
    queryset = Borrowing.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset
