from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.utils import timezone
from books.models import Book
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField(
        validators=[MinValueValidator(timezone.now().date())],
    )
    actual_return_date = models.DateField(null=True, blank=True)
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
        return f"{self.user.email} | {self.book.title} ({self.borrow_date})"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            is_new = not self.pk

            if is_new:
                if self.expected_return_date < date.today():
                    raise ValidationError("Date of return must be in the future")

                if self.book.inventory < 1:
                    raise ValidationError("This book is out of stock")

                self.book.inventory -= 1
                self.book.save()

            super().save(*args, **kwargs)
