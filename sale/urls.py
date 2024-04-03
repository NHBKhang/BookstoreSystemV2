from django.urls import path
from sale import views


urlpatterns = [
    path('', views.index, name='sale'),
    path('api/cart/', views.add_to_sale_cart, name='add_to_sale_cart'),
    path('api/cart/<str:book_id>/', views.alter_sale_cart, name='alter_sale_cart'),
    path('invoice/', views.invoice, name='invoice'),
    path('invoice/return/', views.invoice_return, name='invoice_return'),
    path('invoice/export/', views.export_invoice, name='export_invoice'),
]
