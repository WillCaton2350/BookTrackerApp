from django.urls import path
from .views import index

urlpatterns = [
    path('',index.home_page,name='index.html'),
    path('index',index.home_page,name='index'),
    path('library',index.library,name='library'),
    path('book/<int:id>/download', index.book_download, name='book_download'),
    path('Reviews',index.Reviews,name='Reviews'),
]
