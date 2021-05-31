from django.db import models
from django.db.models.deletion import CASCADE, SET_DEFAULT
from django.contrib.auth.models import User

# django에서 지원하는 User model 사용
'''
# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=200, null=False, primary_key=True)
    user_name = models.CharField(max_length=200, null=False)
    user_password = models.CharField(max_length=200, null=False)
    user_dob = models.DateTimeField(default="", null=False)
    user_create_date = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.user_name
'''
class Bookmark(models.Model):
    book_user =  models.ForeignKey(User, on_delete=CASCADE, null=False)
    book_board_url = models.CharField(max_length=500, null=False)

# 게시글에 대한 작성자확인이 필요할까? 모든 게시글은 admin이 작성할 것인데
class Post(models.Model):
    title = models.CharField(max_length=100, null=False)
    category = models.CharField(max_length=100, null=False)
    content = models.TextField(max_length=5000, null=False)
    # writer_id = models.ForeignKey(User, on_delete=SET_DEFAULT, default="")
    post_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Comment(models.Model):
    # 고유번호는 comment.id로 참조 : id = models.AutoField(primary_key=True)
    comment_content = models.CharField(max_length=500, null=False)
    com_board_url = models.CharField(max_length=500, null=False)
    user_id = models.ForeignKey(User, on_delete=CASCADE, null=False)
    post_id = models.ForeignKey(Post, on_delete=CASCADE, null=False)    # 게시글 고유번호
    com_create_date = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.comment_content