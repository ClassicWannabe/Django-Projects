from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class UserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username','email','password1','password2')

        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            self.fields['username'].label = 'Display Name'
            self.fields['email'].email = 'Email Address'
