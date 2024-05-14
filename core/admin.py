from django.contrib import admin
from django.template.response import TemplateResponse
from core.models import *
from core.forms import BookForm, OrderForm, ReceiptForm
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


admin_site = MyAdminSite(name='myapp')


class DiscountInline(admin.TabularInline):
    model = Discount


class InventoryInline(admin.TabularInline):
    model = Book_Inventories
    min_num = 1
    extra = 1


class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'price', 'active']
    search_fields = ['name', 'description']
    list_filter = ['id', 'name', 'published_date']
    readonly_fields = ['my_image', 'my_qr_code']
    inlines = [InventoryInline, DiscountInline]
    form = BookForm

    def my_image(self, book):
        if book.image:
            return mark_safe(f"<img width='200' src='{book.image}' />")

    def my_qr_code(self, book):
        if book.qr_code:
            return mark_safe(f"<img width='200' src='../../../../../static/{book.qr_code}' />")


class OrderDetailsInline(admin.TabularInline):
    model = OrderDetails
    min_num = 1
    extra = 2


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'tax_fee', 'shipping_fee', 'status', 'customer_user', 'transaction']
    search_fields = ['customer_user', 'transaction']
    list_filter = ['id', 'status']
    readonly_fields = ['customer_user', 'transaction']
    form = OrderForm
    inlines = [OrderDetailsInline]


class ReceiptDetailsInline(admin.TabularInline):
    model = ReceiptDetails
    min_num = 1
    extra = 0


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['id', 'tax_fee', 'shipping_fee', 'customer_user', 'staff_user', 'transaction']
    search_fields = ['customer_user', 'staff_user', 'transaction']
    list_filter = ['id']
    readonly_fields = ['customer_user', 'transaction']
    form = ReceiptForm
    inlines = [ReceiptDetailsInline]


admin_site.register(Group)
admin_site.register(User)
admin_site.register(Category)
admin_site.register(Author)
admin_site.register(Inventory)
admin_site.register(Book_Inventories)
admin_site.register(Book, BookAdmin)
admin_site.register(Order, OrderAdmin)
admin_site.register(OrderDetails)
admin_site.register(Discount)
admin_site.register(Comment)
admin_site.register(Receipt, ReceiptAdmin)
admin_site.register(ReceiptDetails)
