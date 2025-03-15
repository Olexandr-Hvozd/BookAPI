from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BookSerializer
from .models import Books, Category
from rest_framework.decorators import action
from rest_framework.response import Response


class BookViewSet(viewsets.ModelViewSet):
    """
    This viewset provides CRUD operations for the Book model.
    It includes extra actions for searching books by author, title, and category.
    """
    queryset = Books.objects.all()
    serializer_class = BookSerializer
        
    @action(methods=['get'], detail=False, url_path='author/(?P<authors>[^/]+)')
    def author(self, request, authors=None):
        """
        This action allows you to get books by a specific author.

        URL Example:
        /api/v1/books/author/author_name/

        Parameters:
        - authors (str): The name of the author you want to search for.

        Returns:
        - A list of books written by the specified author.
        """
        author = Books.objects.filter(author=authors)

        if not author.exists():
            return Response({"detail": "Author not found"}, status=404)

        book_serializers = BookSerializer(author, many=True)
        return Response(book_serializers.data)
    
    
    @action(methods=['get'], detail=False, url_path='search-by-title')
    def search_by_title(self, request):
        """
        This action allows you to search for a book by its title.

        URL Example:
        /api/v1/books/search-by-title/?title=Book Title

        Parameters:
        - title (str): The title of the book you want to search for.

        Returns:
        - A book object if the title is found, or an error message if the book is not found.
        """
        title = request.query_params.get('title', None)

        if not title:
            return Response({"detail": "Title parameter is required"}, status=400)

        book = Books.objects.filter(title__exact=title).first()

        if not book:
            return Response({"detail": "Book not found with this title"}, status=404)
        
        book.views += 1
        book.save()

        serializer = BookSerializer(book)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='search-by-cat')
    def search_by_cat(self, request):
        """
        This action allows you to search for books by category.

        URL Example:
        /api/v1/books/search-by-cat/?cat=1

        Parameters:
        - cat (int): The ID of the category to search for.

        Returns:
        - A list of books from the specified category, or an error if the category doesn't exist.
        """
        cat = request.query_params.get('cat', None)

        if not cat:
            return Response({'details': "name parameter is required"})
        
        books = Books.objects.filter(cat=cat)

        if not books:
            return Response({'detail': 'category not found with this name'})
        
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)



