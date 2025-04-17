from django.urls import path
from borrowings.views import (
    BorrowingListRetrieveView,
)

app_name = "borrowings"

urlpatterns = [
    path("", BorrowingListRetrieveView.as_view(), name="borrowing_list_retrieve")
]
