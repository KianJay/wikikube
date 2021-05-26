from django.shortcuts import render
from django.http import HttpResponseRedirect
from k8s_doc.models import User, Comment, Post
from k8s_doc.forms import CommentForm
from django.shortcuts import render, redirect
from django.contrib import messages


"""
Form 인스턴스는 is_valid() 함수를 갖고 있음. is_valid() 함수는 입력받은 폼에 대한 유효성 검사를 실행
is_valid() 함수가 호출되면 값이 유효하다면 참이 리턴되고 cleaned_data에 값이 저장
"""

def addComment(request, post_id):
    form = CommentForm(request.POST)

    if not request.session.get("loginuser"):                # 로그인이 안돼있을 경우
        return HttpResponseRedirect("/board/login")
    else :
        if request.method == 'POST' or form.is_valid() :    # 유효성 검사 통과했을 경우
            user_id = request.session.get('loginid')        # 유저 아이디 호출

            # 댓글 작성
            # POST를 통해 댓글 내용을 업로드하고, get으로 게시글의 id와 유저 id를 가져옴
            comment = Comment.objects.create(comment_content=request.POST['comment_content'], com_board=Board.objects.get(pk=board_id), com_user=User.objects.get(pk=user_id))
            comment.save()                                  # 댓글 저장
            return HttpResponseRedirect('/board/boardDetail/' + str(board_id))

        else :
            return HttpResponseRedirect('/board/boardDetail/' + str(board_id))

def editComment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)                        # 댓글 id 호출
    if comment.com_user_id == request.session.get("loginid"):           # 현재 로그인된 아이디와 작성된 댓글의 아이디가 동일하다면
        if request.method == "POST":
            comment.comment_content = request.POST['comment_content']   # 작성한 댓글 내용 업로드
            comment.save()                                              # 댓글 저장
            board_id = comment.com_board_id
            return redirect('/board/boardDetail/' + str(board_id))      # 댓글 수정 후 댓글 작성된 게시글 페이지로 이동
        else :
            return render(request, 'editComment.html')
    else :
        """
        자바스크립트 알람을 통해서 1회성 메시지를 남기는 messages
        HttpRequest를 통해 남기며 1회성이기 때문에 새로고침하면 사라짐
        메시지 출력 방법은 https://ssungkang.tistory.com/entry/Djangomessage-framework-%EC%95%8C%EC%95%84%EB%B3%B4%EA%B8%B0 참고
        """
        messages.error(request, '댓글수정권한이 없습니다')                   # 현재는 축약된 방법으로 메시지를 저장
        return redirect(...)

def deleteComment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    board_id = comment.com_board_id
    if comment.com_user_id == request.session.get("loginid"):  # 현재 로그인된 아이디와 작성된 댓글의 아이디가 동일하다면
        comment.delete()
    else:
        messages.error(request, '댓글삭제권한이 없습니다')
    return redirect('/board/boardDetail/' + str(board_id))

def viewPost(request, post_id):
    # if not request.session.get("loginuser"):
    #     return HttpResponseRedirect("/board/login")
    # 로그인을 안해도 페이지 열람가능
    post = Post.objects.get(pk = post_id)
    comment_list = Comment.objects.all()
    imgSrc = "my_app/" + post.content
    context = { "post":post, "imgSrc" : imgSrc, "comment_list":comment_list }
    return render(request, "postDetail.html", context)

