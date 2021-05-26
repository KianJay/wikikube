from django.urls import path
from k8s_doc import views

urlpatterns = [
    path('postView/<int:post_id>', views.viewPost, name='viewPost'),
    path('addComment/<int:post_id>/', views.addComment, name='addComment'),
    path('editComment/<int:comment_id>/', views.editComment, name='editComment'),
    path('deleteComment/<int:comment_id>', views.deleteComment, name='deleteComment'),
]