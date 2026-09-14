from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import book_model,review_model
from .serializers import book_serializer,review_serializer
import logging
from django.core.paginator import Paginator
from django.http import FileResponse, Http404
import os


'''
If the request is GET then we need to place all of the objects inside a variable (model)
then pass said variable/object to the serializer and return the serialized data as a response.
'''

class index:
    @staticmethod
    def resolve_file_path(uploaded_file):
        if not uploaded_file:
            return None

        file_path = uploaded_file.path

        if not os.path.exists(file_path) and 'uploads/uploads/' in file_path:
            file_path = file_path.replace('uploads/uploads/', 'uploads/')

        return file_path

    def home_page(request):
        books_data = [
            {'image': 'static/images/image1.jpg', 'title': 'Empire of Silence', 'description': 'Christopher Ruocchio'},
            {'image': 'static/images/image8.jpg', 'title': 'Dune', 'description': 'Frank Herbert'},
            {'image': 'static/images/image28.jpg', 'title': 'Jade City', 'description': 'Fonda Lee'},
            {'image': 'static/images/image37.jpg', 'title': 'Red Rising', 'description': 'Pierce Brown'},
            {'image': 'static/images/image31.jpg', 'title': 'Binti', 'description': 'Nnedi Okorafor'},
            {'image': 'static/images/image14.jpg', 'title': 'Black Cake', 'description': 'Charmaine Wilkerson'},
        ]
        paginator = Paginator(books_data, 6)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'index.html', {'page_obj': page_obj})


    def library(request):
        books = book_model.objects.all().order_by('id')

        paginator = Paginator(books, 6)

        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
        }

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        is_htmx = request.META.get('HTTP_HX_REQUEST') == 'true'

        if is_ajax or is_htmx:
            return render(
                request,
                'partials/library_page.html',
                context
            )

        return render(
            request,
            'library.html',
            context
        )
    
    def book_view(request, id):
        try:
            book = book_model.objects.get(pk=id)
        except book_model.DoesNotExist:
            raise Http404("Book Data Model not found")

        if not book.book_file:
            raise Http404("File not found for this book")

        file_path = index.resolve_file_path(book.book_file)
        if not os.path.exists(file_path):
            raise Http404("File missing on disk")

        filename = os.path.basename(book.book_file.name)
        extension = os.path.splitext(filename)[1].lower()
        content_types = {
            '.pdf': 'application/pdf',
            '.epub': 'application/epub+zip',
            '.txt': 'text/plain',
            '.html': 'text/html',
            '.htm': 'text/html',
        }

        response = FileResponse(open(file_path, 'rb'), as_attachment=False, filename=filename)
        response["Content-Type"] = content_types.get(extension, 'application/octet-stream')
        response["Content-Disposition"] = f'inline; filename="{filename}"'
        return response
    
        
    def Reviews(request):
        reviews = review_model.objects.order_by('-review_timestamp')
        return render(request,'Reviews.html',{'reviews':reviews})
    


class BOOK_VALUES:
    @api_view(['GET','POST'])
    def book_list(request,format=None):
        if request.method == 'GET':
            model = book_model.objects.all()
            serializer = book_serializer(model,many=True)
            return Response(serializer.data)
        
        if request.method == 'POST':
            serializer = book_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    @api_view(['GET','PUT','DELETE'])
    def book_detail(request,id,format=None):
        # BASECASE
        try:
            model = book_model.objects.get(pk=id)
        except book_model.DoesNotExist as err:
            logging.error(err)
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = book_serializer(model)
            return Response(serializer.data)
        
        # EXECUTE FUNCTION
        elif request.method == 'PUT':
            serializer = book_serializer(model,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            model.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        

class REVIEW_VALUES:
    @api_view(['GET','POST'])
    def review_list(request,format=None):
        if request.method == 'GET':
            model = review_model.objects.all() 
            # If the request is GET then we need to place all of the objects inside a variable, (model)
            # then pass said variable/object to the serializer and return the serialized data as a response.
            serializer = review_serializer(model,many=True)
            return Response(serializer.data)
        
        # then pass the serialized data from the get REQUEST to the post REQUEST 
        # then check the validity and save the data.
        if request.method == 'POST':
            serializer = review_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



    
    @api_view(['GET','PUT','DELETE'])
    def review_details(request,id,format=None):
        # BASECASE
        try:
            model = review_model.objects.get(pk=id)
        except review_model.DoesNotExist as err:
            logging.error(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
        if request.method == 'GET':
            serializer = review_serializer(model)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = review_serializer(model)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            model.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class PDF_Documents:
    # Both the logic for the search feature and the library book to ereader mappings are contained in this 1:many in_apps_docs() function. (Both use the book_models data models)
    def ereader(request, book_id=None):
        selected_id = book_id if book_id is not None else request.GET.get('book_id') or request.GET.get('doc_id')
        # SEARCH BAR 
        if request.method == 'POST':
            searchbar = request.POST.get('searchbar','').strip()
            # this takes the data entered in to the search bar which is handled by the empty string, targets the searchbar name in the html gets the text from the empty string and posts it to the url as a request? All of this is saved to a searchbar variable.
            if searchbar:
                book = book_model.objects.filter(book_title__icontains=searchbar).first()
                # user defined variable = book_title__iexact ensures that the text data sent through the form is spelled correctly. (exact)
                if book:
                    # if the book variable that holds the text data that is mapped to the book model is true, then store its id in the selected_id variable.
                    selected_id = book.id
                else:
                    book = None
                    # Handles / closes the base case for each if statement
            else:
                book = None
                # ^
        else:
            book = None
            # ^




        # BOOK SELECTION
        documents = list(book_model.objects.all().order_by('id')) 
        # when the 'book_id' on the library.html page is triggered which is mapped to the ereader.html page, view the pdf file inside of the viewer.
        if selected_id: # The HTML and the Admin Panel are linked through the data models (think of it as the way we connected the data models to the admin.py file)
            selected_book = book_model.objects.filter(id=selected_id).first() # This gets the specified book that is mapped from the text data to the id of the book object
        elif documents:
            selected_book = documents[0]  # this line of code is if no specific book is selected, then use the first book as default, aka the object at the 0 index


        pdf_url = None
        if selected_book and selected_book.book_file:
            pdf_url = selected_book.book_file.url

        context = {
            'documents': documents,
            'active': selected_book,
            'selected_id': str(selected_id) if selected_id is not None else None,
            # If the user defined variable selected_id exists then the value in the key value pair that is the selected_id gets type casted to a string. If no value exists then the value is None, not empty.
            'pdf_url': pdf_url,
            'active_pdf_url': pdf_url,
        }

        return render(request, 'ereader.html', context)


 


