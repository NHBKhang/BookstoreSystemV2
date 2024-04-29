from django.contrib import admin
from django.template.response import TemplateResponse
from core.models import Author, Category, Inventory, Book, User, Book_Inventories, Order, OrderDetails, Discount
from core.forms import BookForm, OrderForm
from django.utils.html import mark_safe
from django.urls import path
from core import dao
from django.contrib.auth.models import Group


class MyAdminSite(admin.AdminSite):
    site_header = 'Bookstore Administration'
    site_title = 'Bookstore Administration'

    def get_urls(self):
        return [
            path('books_stats/', self.stats_view),
            path('books_revenue/', self.books_revenue_view)
        ] + super().get_urls()

    def stats_view(self, request):
        return TemplateResponse(request, 'admin/stats.html', {
            'stats': dao.count_books_by_cate()
        })

    def books_revenue_view(self, request):
        return TemplateResponse(request, 'admin/books_revenue.html', {
            'stats': dao.books_revenue()
        })


admin.site = MyAdminSite(name='myapp')


class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'price', 'active']
    search_fields = ['name', 'description']
    list_filter = ['id', 'name', 'published_date']
    readonly_fields = ['my_image', 'my_qr_code']
    form = BookForm

    def my_image(self, book):
        if book.image:
            return mark_safe(f"<img width='200' src='{book.image}' />")

    def my_qr_code(self, book):
        if book.qr_code:
            return mark_safe(f"<img width='200' src='../../../../../static/{book.qr_code}' />")


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'tax_fee', 'shipping_fee', 'status', 'customer_user', 'transaction']
    search_fields = ['customer_user', 'transaction']
    list_filter = ['id', 'status']
    readonly_fields = ['customer_user', 'transaction']
    form = OrderForm


admin.site.register(Group)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Inventory)
admin.site.register(Book_Inventories)
admin.site.register(Book, BookAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetails)
admin.site.register(Discount)
