from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic.base import TemplateView
from k8s_doc.models import Comment, Post, Bookmark #User
from k8s_doc.forms import CommentForm, LoginForm, ForgetpwForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .forms import CreateUserForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail.message import EmailMessage
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm


"""
Form 인스턴스는 is_valid() 함수를 갖고 있음. is_valid() 함수는 입력받은 폼에 대한 유효성 검사를 실행
is_valid() 함수가 호출되면 값이 유효하다면 참이 리턴되고 cleaned_data에 값이 저장
"""

def addComment(request):
    form = CommentForm(request.POST)
    # print()
    # print(request.POST.get('user_id'))
    # print()

    if not request.POST.get('user_id') :              # 로그인이 안돼있을 경우
        return HttpResponseRedirect('../../accounts/login/')
        # return render(request, 'login.html')
    else:
        if request.method == 'POST' or form.is_valid() :    # 유효성 검사 통과했을 경우
            post_id = request.POST.get('post_id', '').strip()
            user_id = request.user        # 유저 아이디 호출
            post = Post.objects.get(pk=post_id)

            # 댓글 작성
            # POST를 통해 댓글 내용을 업로드하고, get으로 게시글의 id와 유저 id를 가져옴
            comment = Comment.objects.create(comment_content=request.POST['comment_content'], post_id=Post.objects.get(pk=post_id), user_id=user_id)
            comment.save()                                  # 댓글 저장
            return redirect('docs:postView', post_id=post.id)

        else:
            return redirect(request.META['HTTP_REFERER'])


def movetoEditComment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)  # 댓글 호출
    if comment.user_id == request.user:  # 현재 로그인된 아이디와 작성된 댓글의 아이디가 동일하다면
        return render(request, 'editComment.html', {'comment': comment})
    else:
        """
        자바스크립트 알람을 통해서 1회성 메시지를 남기는 messages
        HttpRequest를 통해 남기며 1회성이기 때문에 새로고침하면 사라짐
        메시지 출력 방법은 https://ssungkang.tistory.com/entry/Djangomessage-framework-%EC%95%8C%EC%95%84%EB%B3%B4%EA%B8%B0 참고
        """
        messages.error(request, '댓글수정권한이 없습니다')                   # 현재는 축약된 방법으로 메시지를 저장
        return redirect('docs:postView', str(comment.post_id))


def editComment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)                        # 댓글 호출

    if request.method == "POST":
        comment.comment_content = request.POST['comment_content']   # 작성한 댓글 내용 업로드
        # comment.com_create_date = timezone.now()
        comment.save()                                              # 댓글 저장
        post_id = comment.post_id
        return redirect('docs:postView', post_id=post_id)             # 댓글 수정 후 댓글 작성된 게시글 페이지로 이동
    else:
        return render(request, 'editComment.html')


def deleteComment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    post_id = comment.post_id
    if comment.user_id == request.user:  # 현재 로그인된 아이디와 작성된 댓글의 아이디가 동일하다면
        comment.delete()
    else:
        messages.error(request, '댓글삭제권한이 없습니다')
    return redirect('docs:postView', str(comment.post_id))

def viewPost(request, category, title ):
    # if not request.session.get("loginuser"):
    #     return HttpResponseRedirect("/board/login")
    # 로그인을 안해도 페이지 열람가능
    # post = Post.objects.get(category=category, title=title)
    post = get_object_or_404(Post, category=category, title=title)
    comments = Comment.objects.filter(post_id=post)
    # content = post.content
    # imgSrc = "my_app/" + post.content
    # context = {'content': content, 'comments': comments}
    context = {'post': post, 'comments': comments}
    return render(request, "postDetail.html", context)
    # return HttpResponseRedirect(reverse('docs:viewPost', kwargs={'category': category, 'title': title}))


def viewLogin(request):
    return render(request, 'login.html')

# def test(request):
#     return render(request, 'test.html')


# joeunvit

# 회원가입 
# html : signup.html / login.html
# POST : login_id / login_pw / pw_confirm / login_name / login_birth
class CreateUserView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('create_user_done')


class RegisteredView(TemplateView):
    template_name = 'registration/signup_done.html'



def index(request):
    # post_list = Post.objects.all().order_by('-id')[0:10]
    # post = post_list[0]
    # context = {"post":post}

    # context = {"post_list" : post_list}
    # return render(request, 'index.html', context)
    return render(request, 'index.html')

def feedback(request):
    # post_list = Post.objects.all().order_by('-id')[0:10]
    # post = post_list[0]
    # context = {"post":post}

    # context = {"post_list" : post_list}
    # return render(request, 'index.html', context)
    return render(request, 'feedback.html')

def forgetpw(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        try:
            user = User.objects.get(first_name=first_name, last_name=last_name, email=email)
            if user:
                # update_session_auth_hash(request, user)
                context = {"user":user}
                update_session_auth_hash(request, user)
                form = PasswordChangeForm(user)
                return render(request, 'registration/changepw.html', {'form':form})
        except:
            messages.error(request, f"No matching user")
            return render(request, 'registration/forgetpw.html')
    else:
        form = ForgetpwForm(request)
    return render(request, 'registration/forgetpw.html')

class UserPasswordResetView(PasswordResetView):
    template_name = 'registration/forgetpw.html'
    success_url = reverse_lazy('reset_password_done')
    form_class = ForgetpwForm
    
    def form_valid(self, form):
        if User.objects.filter(email=self.request.POST.get("email"), first_name = self.request.POST.get("first_name"), last_name = self.request.POST.get("last_name")).exists():
            return super().form_valid(form)
        else:
            messages.error(self.request, f"No matching user")
            return render(self.request, 'registration/forgetpw.html')
            
            
class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/resetpassworddone.html'



@login_required
def change_password(request):
    print(request)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/changepw.html', {'form':form})

# def send_email(request):
#     subject = "message"
#     to = ["wikikubernetes@gmail.com"]
#     from_email = "wikikubernetes@gmail.com"
#     message = "email test"
#     EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()


# def login(request):
#     # username = request.POST['login_name']
#     # password = request.POST['login_pw']
#     #
#     # user = authenticate(request, username=username, password=password)
#
#     form = LoginForm(request.POST)
#
#     if form.is_valid():
#         login_id = form.cleaned_data["login_id"]
#         login_pw = form.cleaned_data["login_pw"]
#         print(login_id, login_pw)
#
#         # if user is not None:
#         #     login(request, user)
#         #     return HttpResponseRedirect("/doc/viewIndex/")
#
#         try:
#             user = User.objects.get(pk=login_id, user_password=login_pw)
#             print(user)
#             if user:
#                 request.session["loginuser"] = user.user_name
#                 request.session["loginid"] = user.user_id
#                 return HttpResponseRedirect("/doc/viewIndex/")
#             else:
#                 messages.warning(request, "아이디 또는 비밀번호가 틀렸습니다")
#                 return redirect('/accounts/login/')
#
#         except(User.DoesNotExist):
#             messages.warning(request, "아이디 또는 비밀번호가 틀렸습니다")
#             return redirect('/accounts/login/')
#     else:
#         messages.warning(request, "아이디 또는 비밀번호가 틀렸습니다")
#         return redirect('/accounts/login/')


'''  
    if request.method == 'POST':
        
        if User.objects.filter(user_id=request.POST['login_id']).exists(): # 아이디 중복 체크 
            messages.warning(request, "이미 존재하는 아이디입니다.")
            return redirect('signup.html')

        elif request.POST['login_pw'] == request.POST['pw_confirm']: # 비밀번호, 비밀번호 재입력란 일치하면 (아이디 중복 아니고)
            user = User.objects.create(user_id=request.POST['login_id'], user_name=request.POST['login_name'], user_password=request.POST['login_pw'], user_dob=request.POST['login_birth'])
            user.save()
            return render(request, "login.html")

        else: # 비밀번호, 비밀번호 재입력란 일치하지 않으면
            messages.warning(request, "비밀번호가 서로 다릅니다")
            return redirect('signup.html')

    return render(request, 'signup.html')
'''