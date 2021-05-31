from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

"""
장고는 입력에 대한 처리를 할 수 있도록 폼(form) 기능을 제공

HTML에서 form이란  <form> ... </form> 태그 내에서 우리의 웹사이트를 사용하는 사용자가
데이터를 입력할 수 있도록 하고 서버로 데이터를 보내주는 역할을 제공
"""

class CommentForm(forms.Form) :
    comment_content = forms.CharField(label="댓글", max_length=500, required=True)


class LoginForm(forms.Form) :
    login_id = forms.CharField(label="아이디", max_length=100, required=True)
    login_pw = forms.CharField(label="패스워드", max_length=100, required=True , widget=forms.PasswordInput)    


class CreateUserForm(UserCreationForm):
    name = forms.CharField(required=True) # 필드 추가
    #dob = forms.DateField(required=True)

    class Meta:
        model = User
        fields = ("username", "name", "password1", "password2") #, "dob"
        # widgets = {
        #     'username' : forms.TextInput(attrs={'class': 'form-control id'}),
        #     'name' : forms.TextInput(attrs={'class': 'form-control name'}),
        #     'password1' : forms.TextInput(attrs={'class': 'form-control password1'}),
        #     'password2' : forms.TextInput(attrs={'class': 'form-control password2'}),

        # }

    def save(self, commit=True): # 저장하는 부분 오버라이딩
        user = super(CreateUserForm, self).save(commit=False) # 본인의 부모를 호출해서 저장하겠다.
        
        user.name = self.cleaned_data["name"]
        #user.dob = self.cleaned_data['%Y-%m-%d']
        if commit:
            user.save()
        return user