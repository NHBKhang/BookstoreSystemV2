from core.models import Book


def get_books(kw=None, cate_id=None, page=None, desc=True, limit=None):
    books = Book.objects

    if desc:
        books = books.order_by('-id')
    if limit:
        return books.all()[:limit]
    if kw:
        books = books.filter(name__icontains=kw)
    if cate_id:
        books = books.filter(categories__id=cate_id)
    if page:
        pass

    return books.all()


def get_book_by_id(id):
    return Book.objects.get(pk=id)