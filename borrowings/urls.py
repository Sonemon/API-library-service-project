from django.urls import path
from borrowings.views import (
    BorrowingListRetrieveView, BorrowingCreateView,
)

app_name = "borrowings"

urlpatterns = [
    path("", BorrowingListRetrieveView.as_view(), name="borrowing_list_retrieve"),
    path("create/", BorrowingCreateView.as_view(), name="borrowing_create")
]
