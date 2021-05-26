from django import forms

"""
장고는 입력에 대한 처리를 할 수 있도록 폼(form) 기능을 제공

HTML에서 form이란  <form> ... </form> 태그 내에서 우리의 웹사이트를 사용하는 사용자가 
데이터를 입력할 수 있도록 하고 서버로 데이터를 보내주는 역할을 제공
"""

class CommentForm(forms.Form) :
    comment_content = forms.CharField(label="댓글", max_length=500, required=True)