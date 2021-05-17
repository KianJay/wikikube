from django.db import models
from django.db.models.deletion import CASCADE, SET_DEFAULT

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=200, null=False, primary_key=True)
    user_name = models.CharField(max_length=200, null=False)
    user_password = models.CharField(max_length=200, null=False)
    user_birthday = models.DateTimeField(default="", null=False)
    user_create_date = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.user_name

class Comment(models.Model):
    # 고유번호는 comment.id로 참조 : id = models.AutoField(primary_key=True)
    comment_content = models.CharField(max_length=500, null=False)
    com_board_url = models.CharField(max_length=500, null=False)
    com_user = models.ForeignKey(User, on_delete=SET_DEFAULT, null=False)
    com_create_date = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.comment_content

class Bookmark(models.Model):
    book_user =  models.ForeignKey(User, on_delete=SET_DEFAULT, null=False)
    book_board_url = models.CharField(max_length=500, null=False)