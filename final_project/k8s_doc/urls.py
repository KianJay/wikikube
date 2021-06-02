from django.urls import path
from k8s_doc import views
from . import views
from django.contrib.auth import views as auth_views

app_name = 'docs'

urlpatterns = [
    path('viewPost/<str:category>/<str:title>/', views.viewPost, name='viewPost'),
    path('addComment/', views.addComment, name='addComment'),
    path('editComment/<int:comment_id>/', views.editComment, name='editComment'),
    path('deleteComment/<int:comment_id>', views.deleteComment, name='deleteComment'),
    path('feedback', views.feedback, name='feedback'),
    path('toEditComment/<int:comment_id>/', views.movetoEditComment, name='toEditComment'),
    path('showBookmark', views.showBookmark, name='showBookmark')
    # path('login/', auth_views.LoginView.as_view(), name="login"),
    # path('logout/', auth_views.LogoutView, {'next_page' : ''}),
    # path('viewIndex/', views.viewIndex, name='viewIndex'),
    # path('signup', views.CreateUserView.as_view(), name="signup"),
    # path('signup/done', views.RegisteredView.as_view(), name="create_user_done"),
]