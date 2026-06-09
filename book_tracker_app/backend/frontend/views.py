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
    def home_page(request):
        # Create 7 pages of book placeholders with unique content
        books_data = [
            {'image': 'static/images/image1.jpg', 'title': 'Empire of Silence', 'description': 'Christopher Ruocchio'},
            {'image': 'static/images/image2.jpg', 'title': 'Howling Dark', 'description': 'Christopher Ruocchio'},
            {'image': 'static/images/image3.jpg', 'title': 'Demon in White', 'description': 'Christopher Ruocchio'},
            {'image': 'static/images/image4.jpg', 'title': 'Kingdoms of Death', 'description': 'Christopher Ruocchio'},
            {'image': 'static/images/image5.jpg', 'title': 'Ashes of Man', 'description': 'Christopher Ruocchio'},
            {'image': 'static/images/image6.jpg', 'title': 'Disquiet Gods', 'description': 'Christopher Ruocchio'},
            {'image': 'static/images/image7.jpg', 'title': 'Shadows Upon Time', 'description': 'Christopher Ruocchio'},
            {'image': 'static/images/image8.jpg', 'title': 'Dune', 'description': 'Frank Herbert'},
            {'image': 'static/images/image9.jpg', 'title': 'Dune Messiah', 'description': 'Frank Herbert'},
            {'image': 'static/images/image10.jpg', 'title': 'Children of Dune', 'description': 'Frank Herbert'},
            {'image': 'static/images/image11.jpg', 'title': 'God Emperor Dune', 'description': 'Frank Herbert'},
            {'image': 'static/images/image12.jpg', 'title': 'Heretics of Dune', 'description': 'Frank Herbert'},
            {'image': 'static/images/image13.jpg', 'title': 'Chapterhouse Dune', 'description': 'Frank Herbert'},
            {'image': 'static/images/image14.jpg', 'title': 'Black Cake', 'description': 'Charmaine Wilkerson'},
            {'image': 'static/images/image15.jpg', 'title': 'Good Dirt', 'description': 'Charmaine Wilkerson'},
            {'image': 'static/images/image16.jpg', 'title': 'Blown to Hell', 'description': 'Walter Pinicus'},
            {'image': 'static/images/image17.jpg', 'title': 'Bombs over Bikini', 'description': 'Connie Goldsmith'},
            {'image': 'static/images/image18.jpg', 'title': 'Codependent No More', 'description': 'Melody Beattie'},
            {'image': 'static/images/image19.jpg', 'title': 'Crude Capitalisim', 'description': 'Adam Hanieh'},
            {'image': 'static/images/image20.jpg', 'title': 'Darkwater', 'description': 'W. E. B. Du Bois'},
            {'image': 'static/images/image21.jpg', 'title': 'False War', 'description': 'Carlos Manuel Álvarez'},
            {'image': 'static/images/image22.jpg', 'title': 'Free the Land', 'description': 'Edward Onaci'},
            {'image': 'static/images/image23.jpg', 'title': 'Gaza', 'description': 'Norman Finkelstien'},
            {'image': 'static/images/image24.jpg', 'title': 'Crusade for Justice', 'description': 'Alfreda Duster'},
            {'image': 'static/images/image25.jpg', 'title': 'DSA in Python', 'description': 'Michael Goodrich'},
            {'image': 'static/images/image26.jpg', 'title': 'Palestine', 'description': 'Sumaya Awad'},
            {'image': 'static/images/image27.jpg', 'title': 'Think Again', 'description': 'Adam Grant'},
            {'image': 'static/images/image28.jpg', 'title': 'Jade City', 'description': 'Fonda Lee'},
            {'image': 'static/images/image29.jpg', 'title': 'Jade War', 'description': 'Fonda Lee'},
            {'image': 'static/images/image30.jpg', 'title': 'Jade Legacy', 'description': 'Fonda Lee'},
            {'image': 'static/images/image31.jpg', 'title': 'Binti', 'description': 'Nnedi Okorafor'},
            {'image': 'static/images/image32.jpg', 'title': 'Binti: Home', 'description': 'Nnedi Okorafor'},
            {'image': 'static/images/image33.jpg', 'title': 'Binti: The Night Masquerade', 'description': 'Nnedi Okorafor'},
            {'image': 'static/images/image34.jpg', 'title': 'Project Hailmary', 'description': 'Andy Weir'},
            {'image': 'static/images/image35.jpg', 'title': 'Sword of Kaigen', 'description': 'M.L. Wang'},
            {'image': 'static/images/image36.jpg', 'title': 'Last Contract of Isako', 'description': 'Fonda Lee'},
            {'image': 'static/images/image37.jpg', 'title': 'Red Rising', 'description': 'Pierce Brown'},
            {'image': 'static/images/image38.jpg', 'title': 'Golden Son', 'description': 'Pierce Brown'},
            {'image': 'static/images/image39.jpg', 'title': 'Morning Star', 'description': 'Pierce Brown'},
            {'image': 'static/images/image40.jpg', 'title': 'Iron Gold', 'description': 'Pierce Brown'},
            {'image': 'static/images/image41.jpg', 'title': 'Dark Age', 'description': 'Pierce Brown'},
            {'image': 'static/images/image42.jpg', 'title': 'Lightbringer', 'description': 'Pierce Brown'},
        ]
        paginator = Paginator(books_data, 6)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'index.html', {'page_obj': page_obj})
    
    def library(request):
        # Prefer Book objects if any exist; otherwise use placeholder data
        model_entries = book_model.objects.all()
        if model_entries.exists():
            books_data = []
            for b in model_entries:
                img = None
                try:
                    img = b.book_image.url
                except Exception:
                    img = '/static/images/image1.jpg'
                books_data.append({'id': b.id, 'image': img, 'title': b.book_title, 'description': b.book_author})
    
        paginator = Paginator(books_data, 6)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'library.html', {'page_obj': page_obj})

    def book_download(request, id):
        try:
            book = book_model.objects.get(pk=id)
        except book_model.DoesNotExist:
            raise Http404("Book not found")

        if not book.book_file:
            raise Http404("File not found for this book")

        file_path = book.book_file.path
        
        # Handle old uploads (stored as "uploads/filename.epub")
        # which creates double "uploads/uploads/" when MEDIA_ROOT is "uploads/"
        if not os.path.exists(file_path) and 'uploads/uploads/' in file_path:
            file_path = file_path.replace('uploads/uploads/', 'uploads/')
        
        if not os.path.exists(file_path):
            raise Http404("File missing on disk")

        filename = os.path.basename(book.book_file.name)
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
        
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
        
    


        
