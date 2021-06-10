from django.contrib import admin
from k8s_doc.models import Bookmark, Post, Comment

admin.site.register(Bookmark)
admin.site.register(Post)
admin.site.register(Comment)

# Register your models here.