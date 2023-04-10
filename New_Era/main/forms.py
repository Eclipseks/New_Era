from django import forms
from .models import Upload, Source

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    source = forms.ModelChoiceField(queryset=Source.objects.all())

    class Meta:
        model = Upload
        fields = ['file', 'source']
        