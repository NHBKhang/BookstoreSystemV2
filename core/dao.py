from core.models import Book, Comment
from bookstore import settings


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
        page = int(page)
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        return books[start:start+page_size]

    return books.all()


def books_count(cate_id=None, kw=None):
    books = Book.objects

    if cate_id:
        books = books.filter(categories__id=cate_id)
    if kw:
        books = books.filter(name__icontains=kw)

    return books.count()


def get_book_by_id(id):
    return Book.objects.get(pk=id)


def get_comments(book_id):
    return Comment.objects.filter(book_id=book_id)


def save_comment(book_id, user_id, content):
    comment = Comment.objects.create(book_id=book_id, user_id=user_id, content=content)
    return comment
