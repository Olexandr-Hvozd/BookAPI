from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BookSerializer
from .models import Books, Category
from rest_framework.decorators import action
from rest_framework.response import Response


class BookViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
        
    @action(methods=['get'], detail=False, url_path='author/(?P<authors>[^/]+)')
    def author(self, request, authors=None):
        author = Books.objects.filter(author=authors)

        if not author.exists():
            return Response({"detail": "Author not found"}, status=404)

        book_serializers = BookSerializer(author, many=True)
        return Response(book_serializers.data)
    
    
    @action(methods=['get'], detail=False, url_path='search-by-title')
    def search_by_title(self, request):
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


