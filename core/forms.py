from django import forms
from core.models import Book, User


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
