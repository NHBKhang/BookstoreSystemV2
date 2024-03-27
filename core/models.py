from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
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
