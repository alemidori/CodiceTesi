from django import forms

class UploadFileForm(forms.Form):
    name_file = forms.FileField(label="", label_suffix="inputId")
    #title = forms.CharField(max_length=50)
    #file = forms.FileField()