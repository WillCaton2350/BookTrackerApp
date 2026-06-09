from django.contrib import admin
from django.urls import path, include
from frontend.views import BOOK_VALUES,REVIEW_VALUES
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('frontend.urls')),
    path('books/',BOOK_VALUES.book_list),
    path('books/<int:id>',BOOK_VALUES.book_detail),
    path('reviews/',REVIEW_VALUES.review_list),
    path('reviews/<int:id>',REVIEW_VALUES.review_details)
    
]

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
