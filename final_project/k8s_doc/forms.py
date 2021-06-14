from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, _unicode_ci_compare
from django.forms import fields
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

"""
장고는 입력에 대한 처리를 할 수 있도록 폼(form) 기능을 제공

HTML에서 form이란  <form> ... </form> 태그 내에서 우리의 웹사이트를 사용하는 사용자가
데이터를 입력할 수 있도록 하고 서버로 데이터를 보내주는 역할을 제공
"""

class CommentForm(forms.Form):
    comment_content = forms.CharField(label="댓글", max_length=500, required=True)


class LoginForm(forms.Form):
    login_id = forms.CharField(label="아이디", max_length=100, required=True)
    login_pw = forms.CharField(label="패스워드", max_length=100, required=True , widget=forms.PasswordInput)    


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(required=True) # 필드 추가
    last_name = forms.CharField(required=True) # 필드 추가
    email = forms.EmailField(max_length=30, required=True)
    # dob = forms.DateField() # input_formats=['%Y-%m-%d']

    class Meta:
        model = User
        fields = ("username", "first_name", 'last_name', 'email', "password1", "password2") #, 'dob'

    def save(self, commit=True): # 저장하는 부분 오버라이딩
        user = super(CreateUserForm, self).save(commit=False) # 본인의 부모를 호출해서 저장하겠다.
        
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        # user.dob = self.cleaned_data["date"]

        if commit:
            user.save()
        return user

UserModel = get_user_model()

class ForgetpwForm(PasswordResetForm):
    first_name = forms.CharField(label="first_name", max_length=100, required=True)
    last_name = forms.CharField(label="last_name", max_length=100, required=True)

    class Meta:
        fields = ['first_name', 'last_name', 'email']

    def get_users(self, first_name, last_name, email):
        email_field_name = UserModel.get_email_field_name()
        # active_users = UserModel._default_manager.filter(**{
        #     '%s__iexact' % email_field_name: email,
        #     'is_active': True,
        # })
        # print(self)
        # print(email)
        # print(self.first_name)
        # print(self.last_name)
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % email_field_name: email,
            '%s__iexact' % "first_name": first_name,
            '%s__iexact' % "last_name": last_name,
            'is_active': True,
        })
        print(active_users)
        return (
            u for u in active_users
            if u.has_usable_password() and
            _unicode_ci_compare(email, getattr(u, email_field_name))
        )

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        email_field_name = UserModel.get_email_field_name()
        for user in self.get_users(first_name, last_name, email):
            user_email = getattr(user, email_field_name)
            context = {
                'email': user_email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                user_email, html_email_template_name=html_email_template_name,
            )


class Feedbackform(forms.Form):
    name = forms.CharField(label="name", max_length=500)
    email = forms.EmailField(label="email", max_length=500)
    message = forms.CharField(label="message", max_length=500)

    class Meta:
        fields = ['name', 'email', 'message']


class PostSearchForm(forms.Form):
    search_word = forms.CharField(label='Search Word')