from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    COVER_CHOICES = [
        ("HARD", "Hardcover"),
        ("SOFT", "Softcover"),
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=4, choices=COVER_CHOICES)
    inventory = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    daily_fee = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(0)]
    )

    class Meta:
        ordering = ["title"]
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author", "cover"],
                name="unique_book_title_author_cover",
            )
        ]

    def __str__(self):
        return f"{self.title} by {self.author}"
