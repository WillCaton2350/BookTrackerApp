from rest_framework import serializers
from .models import book_model, review_model

class book_serializer(serializers.ModelSerializer):
    class Meta:
        model = book_model
        fields = [
        'book_title',
        'book_author',
        'page_number',
        'book_format',
        'book_image',
        'book_price',
        'book_file'
        ]

        

class review_serializer(serializers.ModelSerializer):
    class Meta:
        model = review_model
        fields = [
            'book_review_title',
            'book_review_author',
            'review_rate',
            'review_description',
            'review_timestamp',
            'review_book_image'
            ]