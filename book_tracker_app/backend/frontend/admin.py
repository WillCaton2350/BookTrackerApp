from django.contrib import admin
from frontend.models import book_model, review_model


admin.site.register(book_model)
admin.site.register(review_model)

