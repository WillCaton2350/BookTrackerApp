from django.urls import path
from .views import index, PDF_Documents

urlpatterns = [
    path('', index.home_page, name='index.html'),
    path('index', index.home_page, name='index'),
    path('library', index.library, name='library'),
    path('Reviews', index.Reviews, name='Reviews'),
    path('Documents', PDF_Documents.ereader, name='docs'),
    path('Documents/', PDF_Documents.ereader, name='docs_slash'),
    path('Documents/<int:book_id>/', PDF_Documents.ereader, name='docs_by_id'),
]
