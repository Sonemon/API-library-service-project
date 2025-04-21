from django.urls import path
from borrowings.views import (
    BorrowingListView,
    BorrowingRetrieveView,
    BorrowingCreateView,
    BorrowingReturnView
)

app_name = "borrowings"

urlpatterns = [
    path("", BorrowingListView.as_view(), name="borrowing_list"),
    path("create/", BorrowingCreateView.as_view(), name="borrowing_create"),
    path("<int:pk>/", BorrowingRetrieveView.as_view(), name="borrowing_detail"),
    path("<int:pk>/return/", BorrowingReturnView.as_view(), name="borrowing_return"),
]
