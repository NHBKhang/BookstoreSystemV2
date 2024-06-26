from django import forms
from core.models import Book, User, Order, Receipt


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = '__all__'
