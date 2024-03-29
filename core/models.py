from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django_enumfield import enum


class Gender(enum.Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3


class User(AbstractUser):
    avatar = CloudinaryField(null=True,
                             default="https://res.cloudinary.com/dd0qzygo7/image/upload/v1711539545/gyaplslq1shp2exulcia.png")
    birthday = models.DateField(null=True)
    gender = enum.EnumField(Gender, default=Gender.MALE)
    phone = models.CharField(max_length=11, null=True)
    address = models.TextField(null=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "inventories"


class Book(models.Model):
    name = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='books')
    authors = models.ManyToManyField(Author, related_name='books')
    inventories = models.ManyToManyField(Inventory, through='Book_Inventories', related_name='books')

    def __str__(self):
        return self.name


class Book_Inventories(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = "books belong to inventories"
        verbose_name_plural = "books belong to inventories"

    def __str__(self):
        return self.book.name + " thuộc kho " + self.inventory.name


class Comment(models.Model):
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


class Transaction(models.Model):
    transaction_id = models.BigIntegerField(null=False, blank=False)
    transaction_date = models.DateTimeField(auto_now_add=True)
    bank_code = models.CharField(max_length=20, null=False, blank=False)
    description = models.TextField(null=False)


class ItemBase(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    tax_fee = models.IntegerField(null=False, blank=False, default=1000)
    shipping_fee = models.IntegerField(null=False, blank=False, default=1000)

    class Meta:
        abstract = True
        ordering = ['-id']


class ItemDetailsBase(models.Model):
    quantity = models.IntegerField(null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)

    class Meta:
        abstract = True
        ordering = ['-id']


class OrderStatus(enum.Enum):
    PENDING = 1
    PROCESSING = 2
    SHIPPED = 3
    DELIVERED = 4
    CANCELLED = 5


class Order(ItemBase):
    updated_date = models.DateTimeField(auto_now=True)
    status = enum.EnumField(OrderStatus, null=False, blank=False, default=OrderStatus.PENDING)
    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True, blank=True, related_name='orders')

    def __str__(self):
        return 'Đơn hàng ' + str(self.id)


class OrderDetails(ItemDetailsBase):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='order_details')


class Receipt(ItemBase):
    staff_user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receipts')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='receipts')

    def __str__(self):
        return 'Hóa đơn ' + str(self.id)


class ReceiptDetails(ItemDetailsBase):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='receipt_details')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='receipt_details')

# class DiscountBase(models.Model):
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     valid_from = models.DateTimeField(null=True, blank=True)
#     valid_to = models.DateTimeField(null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.code
#
#     def is_valid(self):
#         now = timezone.now()
#         return self.valid_from <= now <= self.valid_to


# class DiscountCode(models.Model):
#     code = models.CharField(max_length=20, unique=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     valid_from = models.DateTimeField(null=True, blank=True)
#     valid_to = models.DateTimeField(null=True, blank=True)
#     is_active = models.BooleanField(default=True)
