from django import forms


class FileForm(forms.Form):
    file_name = forms.CharField(label='File name', max_length=100)
    file_body = forms.FileField(label='File body')
