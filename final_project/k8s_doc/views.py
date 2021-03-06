from django.db.models import Q
from django.shortcuts import get_object_or_404, render, resolve_url, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url, urlsafe_base64_decode
# from django.views.generic import TemplateView
from django.views import generic, View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from django.views.decorators.http import require_POST
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash, get_user_model, REDIRECT_FIELD_NAME, logout as auth_logout
from django.contrib.auth.models import User, AnonymousUser 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .forms import CreateUserForm, Feedbackform, PostSearchForm
from django.urls import reverse_lazy, reverse
from django.core.mail.message import EmailMessage
from django.core.exceptions import ValidationError
from django.conf import settings
from django.template import RequestContext
import tkinter
from tkinter import messagebox

try:
    from django.utils import simplejson as json
except ImportError:
    import json


from k8s_doc.models import Comment, Post, Bookmark #User
from k8s_doc.forms import CommentForm, LoginForm, ForgetpwForm

"""
Form 인스턴스는 is_valid() 함수를 갖고 있음. is_valid() 함수는 입력받은 폼에 대한 유효성 검사를 실행
is_valid() 함수가 호출되면 값이 유효하다면 참이 리턴되고 cleaned_data에 값이 저장
"""

@login_required
def addComment(request):
    form = CommentForm(request.POST)

    if not request.user.is_authenticated:              # 로그인이 안돼있을 경우 not request.user
        return HttpResponseRedirect('../../accounts/login/')
    else:
        if request.method == 'POST' or form.is_valid() :    # 유효성 검사 통과했을 경우
            post_id = request.POST.get('post_id', '').strip()
            user_id = request.user        # 유저 아이디 호출
            post = Post.objects.get(pk=post_id)

            # 댓글 작성
            # POST를 통해 댓글 내용을 업로드하고, get으로 게시글의 id와 유저 id를 가져옴
            comment = Comment.objects.create(comment_content=request.POST['comment_content'], post_id=Post.objects.get(pk=post_id), user_id=user_id)
            comment.save()                                  # 댓글 저장
            return redirect('docs:viewPost', post.category, post.title)

        else:
            return redirect(request.META['HTTP_REFERER'])

@login_required
def movetoEditComment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)  # 댓글 호출
    post_id = comment.post_id

    if not request.user.is_authenticated:
        messages.error(request, '댓글수정권한이 없습니다')                   # 현재는 축약된 방법으로 메시지를 저장
        return redirect('docs:viewPost', post_id.category, post_id.title)
    else:
        if comment.user_id == request.user:  # 현재 로그인된 아이디와 작성된 댓글의 아이디가 동일하다면
            return render(request, 'editComment.html', {'comment': comment})
        else:
            root = tkinter.Tk()
            root.withdraw()

            messagebox.showerror('권한 없음', '댓글을 수정할 권한이 없습니다.')

            """
            자바스크립트 알람을 통해서 1회성 메시지를 남기는 messages
            HttpRequest를 통해 남기며 1회성이기 때문에 새로고침하면 사라짐
            메시지 출력 방법은 https://ssungkang.tistory.com/entry/Djangomessage-framework-%EC%95%8C%EC%95%84%EB%B3%B4%EA%B8%B0 참고
            """
            # messages.error(request, '댓글수정권한이 없습니다')                   # 현재는 축약된 방법으로 메시지를 저장
            return redirect('docs:viewPost', post_id.category, post_id.title)

@login_required
def editComment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)                        # 댓글 호출
    post_id = comment.post_id

    if request.method == "POST":
        comment.comment_content = request.POST['comment_content']   # 작성한 댓글 내용 업로드
        comment.save()                                              # 댓글 저장
        post_id = comment.post_id
        return redirect('docs:viewPost', post_id.category, post_id.title) # 댓글 수정 후 댓글 작성된 게시글 페이지로 이동
    else:
        return render(request, 'editComment.html')

@login_required
def deleteComment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    post_id = comment.post_id

    if comment.user_id == request.user:  # 현재 로그인된 아이디와 작성된 댓글의 아이디가 동일하다면
        comment.delete()
    else:
        root = tkinter.Tk()
        root.withdraw()

        messagebox.showerror('권한 없음', '댓글을 삭제할 권한이 없습니다.')
    return redirect('docs:viewPost', post_id.category, post_id.title)


def viewPost(request, category, title ):
    # 로그인을 안해도 페이지 열람가능

    post = get_object_or_404(Post, category=category, title=title)
    comments = Comment.objects.filter(post_id=post)

    if request.user.is_authenticated: # 사용자가 로그인 상태일 때
        if Bookmark.objects.filter(book_user=request.user, post_id=post.id) is not None:
            context = {'post': post, 'comments': comments, 'bookmark': Bookmark.objects.filter(book_user=request.user, post_id=post.id)}
            return render(request, "postDetail.html", context)
    else:
        context = {'post': post, 'comments': comments}
        return render(request, "postDetail.html", context)


def viewLogin(request):
    return render(request, 'login.html')

@login_required
def showBookmark(request):
    if not request.user.is_authenticated:              # 로그인이 안돼있을 경우
        return HttpResponseRedirect('../../accounts/login/')
    else:
        bl = Bookmark.objects.filter(book_user=request.user)

        postlist = []
        kotitlelist = []
        for book in bl:
            postlist.append(book.post_id)
            test = book.post_id.content.split('\n')
            kotitlelist.append(test[0].strip('#'))
        zippedlist = zip(postlist,kotitlelist)
        context = {'bl': bl, 'zippedlist':zippedlist}
        return render(request, 'bookmark.html', context)

@login_required
def addBookmark(request):
    post_id = request.POST['post_id']
    post = Post.objects.get(pk=post_id)
    bookmark = Bookmark.objects.create(book_user=request.user, post_id=post)
    bookmark.save()
    return redirect('docs:viewPost', post.category, post.title)

@login_required
def delBookmark(request):
    post_id = request.POST['post_id']
    post = Post.objects.get(pk=post_id)
    bookmark = Bookmark.objects.get(book_user=request.user, post_id=post)
    bookmark.delete()
    return redirect('docs:viewPost', post.category, post.title)


# joeunvit

# 회원가입 
# html : signup.html / login.html
# POST : login_id / login_pw / pw_confirm / login_name / login_birth
class CreateUserView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('create_user_done')

def index(request):
    return render(request, 'index.html')

class UserPasswordResetView(PasswordResetView):
    template_name = 'registration/forgetpw.html'
    success_url = reverse_lazy('reset_password_done')
    form_class = ForgetpwForm
    
    def form_valid(self, form):
        try:
            User.objects.get(email=self.request.POST.get("email"), first_name = self.request.POST.get("first_name"), last_name = self.request.POST.get("last_name"))
            return super().form_valid(form)
        except:
            messages.error(self.request, f"No matching user")
            return render(self.request, 'registration/forgetpw.html')
                        
class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/resetpassworddone.html'

UserModel = get_user_model()
INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = SetPasswordForm
    success_url=reverse_lazy('reset_password_complete')
    template_name = 'registration/password_reset_confirm.html'

    def form_valid(self, form):
        return super().form_valid(form)

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/resetpasswordcomplete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context

@login_required
def change_password(request):
    print(request)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            # messages.success(request, 'Your password was successfully updated!')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/changepw.html', {'form':form})
 
def search(request):

    q = request.GET.get('q', "")
    print(q)

    if q:
        posts = Post.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).distinct()
        contentlist = []
        for post in posts:
            test = post.content.split('\n')
            contentlist.append(test[0].strip('#'))
        zippedlist = zip(posts, contentlist)
        return render(request, 'search.html', {'zippedlist': zippedlist, 'q': q})

    else:
        return render(request, 'search.html')