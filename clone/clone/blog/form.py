from .models import BloggerContent
from django import forms
from ckeditor.widgets import CKEditorWidget

class Blo(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = BloggerContent
        fields = '__all__'