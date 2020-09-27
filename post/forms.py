from django import forms
from .models import Post,Image

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('name','text','group')



class PostImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields =  ('picture',)

        widgets = {
            'picture':forms.ClearableFileInput(attrs={'multiple':True})
        }
