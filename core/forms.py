from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from core.models import Book


class BookForm(forms.ModelForm):
    # description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Book
        fields = '__all__'