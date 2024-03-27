from rest_framework import viewsets, generics, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from core import serializers, paginators, dao
from core.models import Category, User, Author, Inventory, Book, Book_Inventories
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import math, json
from bookstore import settings
from core.utils import context_processors as cp


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class AuthorViewSet(viewsets.ViewSet, generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer


class InventoryViewSet(viewsets.ViewSet, generics.RetrieveUpdateAPIView, generics.ListAPIView):
    queryset = Inventory.objects.all()
    serializer_class = serializers.InventorySerializer


class BookInventoriesViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Book_Inventories.objects.all()
    serializer_class = serializers.BookInventoriesSerializer


class BookViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Book.objects.filter(active=True)
    serializer_class = serializers.BookSerializer
    pagination_class = paginators.BookPaginator

    def get_queryset(self):
        queryset = self.queryset

        if self.action.__eq__('list'):
            q = self.request.query_params.get('q')
            if q:
                queryset = queryset.filter(name__icontains=q)

            cate_id = self.request.query_params.get('category_id')
            if cate_id:
                queryset = queryset.filter(category_id=cate_id)

        return queryset

    @action(methods=['get'], url_path='lessons', detail=True)
    def get_lessons(self, request, pk):
        lessons = self.get_object().lesson_set.filter(active=True)

        q = request.query_params.get('q')
        if q:
            lessons = lessons.filter(subject__icontains=q)

        return Response(serializers.LessonSerializer(lessons, many=True).data,
                        status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser, ]


# template
def index(request):
    books = dao.get_books(limit=4)

    return render(request, 'index.html', {'books': books})


def pages(request):
    cate_id = request.GET.get('cate_id')
    page = request.GET.get('page')
    kw = request.GET.get('kw')

    books = dao.get_books(cate_id=cate_id, kw=kw, page=page)

    return render(request, 'pages.html', {
        'books': books,
        'pages': math.ceil(books.count() / settings.PAGE_SIZE)
    })


def details(request, book_id):
    book = dao.get_book_by_id(book_id)

    return render(request, 'details.html', {
        'book': book,
        'authors': [{'id': item[0], 'name': item[1]} for item in book.authors.values_list('id', 'name')],
        'categories': [{'id': item[0], 'name': item[1]} for item in book.categories.values_list('id', 'name')]
    })


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def cart(request):
    c = request.session.get('cart', {})

    return render(request, 'cart.html', {'cart': c})


def add_to_cart(request):
    if request.method == 'POST':
        cart_key = 'cart'
        cart = request.session.get(cart_key, {})

        data = json.loads(request.body.decode('utf-8'))
        id = str(data.get("id"))

        if id in cart:  # sp da co trong gio
            cart[id]['quantity'] += 1
        else:  # san pham chua co trong gio
            cart[id] = {
                "id": id,
                "name": data.get("name"),
                "price": data.get("price"),
                "quantity": 1,
                # "max_quantity": dao.get_book_inventory(id).quantity
            }

        request.session[cart_key] = cart

        return JsonResponse(cp.count_cart(request))
