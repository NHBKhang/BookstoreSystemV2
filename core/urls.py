from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core import views
from django.contrib.auth import views as auth_views

r = routers.DefaultRouter()
r.register('categories', views.CategoryViewSet, basename='categories')
r.register('authors', views.AuthorViewSet, basename='authors')
r.register('inventories', views.InventoryViewSet, basename='inventories')
r.register('users', views.UserViewSet, basename='users')
r.register('book_inventories', views.BookInventoriesViewSet, basename='book_inventories')
r.register('books', views.BookViewSet, basename='books')

urlpatterns = [
    path('api/', include(r.urls)),
    path('', views.index, name='home'),
    path('books/', views.pages, name='books'),
    path('books/<int:book_id>/', views.details, name='details'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('cart/', views.cart, name='cart'),
    path('api/cart/', views.add_to_cart, name='add_to_cart'),
    path('api/cart/<str:book_id>/', views.alter_cart, name='alter_cart')
]