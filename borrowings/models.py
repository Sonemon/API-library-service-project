from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone
from books.models import Book
from users.models import User


def get_default_expected_return_date():
    return timezone.localdate() + timedelta(days=7)


class Borrowing(models.Model):
    borrow_date = models.DateTimeField(auto_now_add=True)
    expected_return_date = models.DateField(
        default=get_default_expected_return_date,
    )
    actual_return_date = models.DateTimeField(null=True, blank=True)

    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT,
        related_name="borrowings"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="borrowings"
    )

    class Meta:
        ordering = ["-borrow_date"]

    def __str__(self):
        return f"{self.user.email} | {self.book.title} ({self.borrow_date.date()})"

    def clean(self):
        if self.expected_return_date and self.expected_return_date < timezone.localdate():
            raise ValidationError("Expected return date must be in the future.")

        if not self.pk and self.book.inventory < 1:
            raise ValidationError("This book is out of stock.")

    def save(self, *args, **kwargs):
        is_new = not self.pk

        self.full_clean()

        with transaction.atomic():
            if is_new:
                self.book.inventory -= 1
                self.book.save()

            super().save(*args, **kwargs)

    def return_borrowing(self):
        with transaction.atomic():
            if self.actual_return_date:
                raise ValidationError("This book has already been returned.")

            self.book.inventory += 1
            self.book.save()

            self.actual_return_date = timezone.now()
            self.save()
