from django.contrib import admin
from core.models import Author, Category, Inventory, Book
from core.forms import BookForm


class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'price', 'active']
    search_fields = ['name', 'description']
    list_filter = ['id', 'name', 'published_date']
    readonly_fields = ['my_image']
    form = BookForm

    def my_image(self, book):
        if book.image:
            return mark_safe(f"<img width='200' src='{book.image.url}' />")


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Inventory)
admin.site.register(Book, BookAdmin)
