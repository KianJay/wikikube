"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from k8s_doc import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include('k8s_doc.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', views.CreateUserView.as_view(), name="signup"),
    path('accounts/change_password', views.change_password, name='change_password'),
    path('accounts/forgetpw', views.forgetpw, name="forgetpw"),

    # path('accounts/signup/done', views.RegisteredView.as_view(), name="create_user_done"),
    # path('', views.index, name="create_user_done"),
    path('accounts/login/', auth_views.LoginView.as_view(), name="create_user_done"),

    path('', views.index, name="index"),
    path('markdownx/', include('markdownx.urls')),
    path('docs/index', views.index, name="index" ),
]


'''
accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']
'''