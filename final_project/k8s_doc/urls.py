from django.urls import path
from k8s_doc import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('postView/<int:post_id>', views.viewPost, name='viewPost'),
    path('addComment/<int:post_id>/', views.addComment, name='addComment'),
    path('editComment/<int:comment_id>/', views.editComment, name='editComment'),
    path('deleteComment/<int:comment_id>', views.deleteComment, name='deleteComment'),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('homeview/', views.homeview, name='homeview'), # 임시
    path('signup', views.CreateUserView.as_view(), name="signup"),
    path('login/done', views.RegisteredView.as_view(), name="create_user_done"),
]