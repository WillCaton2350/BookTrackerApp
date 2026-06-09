from django.db import models

class book_model(models.Model):
    book_title = models.CharField(max_length=255)
    book_author = models.CharField(max_length=255)
    page_number = models.IntegerField()
    book_format = models.CharField(max_length=255)
    book_image = models.ImageField(upload_to='', null=True, blank=True)
    book_price = models.CharField(max_length=255)
    book_file = models.FileField(upload_to='', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.book_title + ' ' + self.book_author


class review_model(models.Model):
    book_review_title = models.CharField(max_length=255)
    book_review_author = models.CharField(max_length=255)
    review_rate = models.IntegerField()
    review_description = models.TextField(max_length=1000)
    review_timestamp = models.DateTimeField(auto_now_add=True)
    review_book_image = models.ImageField(null=True)

    def __str__(self):
        return f"{self.book_review_title} | {self.book_review_author} | [{self.review_rate}/5]"
        