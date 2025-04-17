from rest_framework import serializers


class BookSerializer(serializers.Serializer):
    class Meta:
        model = "Book"
        fields = (
            "id",
            "title",
            "author",
            "cover",
            "inventory",
            "daily_fee",
        )
