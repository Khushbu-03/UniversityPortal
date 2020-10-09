from django.conf import settings
from django.urls import path
from django.views.static import serve
from django.contrib.auth import views as auth_views
from myapp import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

from myapp.views import profile_image, success

app_name = 'myapp'

urlpatterns = [
    path(r'index/', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    path(r'detail/<top_no>', views.detail, name='detail'),
    path(r'courses/', views.courses, name='courses'),
    path(r'placeorder/', views.placeorder, name='placeorder'),
    path(r'courses/<int:cour_id>/', views.coursedetail, name='coursedetail'),
    path(r'myaccount/', views.myaccount, name="myaccount"),
    path(r'user_login/', views.user_login, name="user_login"),
    path(r'logout', views.user_logout, name="user_logout"),
    path(r'register/', views.register, name='register'),
    path(r'reset_password/', auth_views.PasswordResetView.as_view(template_name="myapp/templates/myapp/forgot-password.html"),
         name="password_reset"),
    path(r'reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path(r'reset_confirm/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path(r'reset_password/', auth_views.PasswordResetView.as_view(), name="password_reset_complete"),
    # path(r'order_confirmed/', views.success(), name="order_confirmation"),
    # path(r'forgot_password/', views.forgot_password, name='forgot_password'),
    # path(r'password_change_form/', views.PasswordResetView, name='PasswordResetView'),
    path(r'media/', serve, {'document_root': settings.MEDIA_ROOT}),
    path(r'image_upload/', views.profile_image, name='profile_image'),
    path(r'success/', success, name = 'success')

]
