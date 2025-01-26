from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),

    path('logout/', views.logout_view, name='logout'),  # URL para logout


    path("reset/password_reset/",auth_views.PasswordResetView.as_view(template_name="password_resete.html",email_template_name="registration/password_reset_email.html"), name="password_reset"),
    path("reset/password_reset/done/",auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),name='password_reset_done'),
    path("reset/reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),name='password_reset_confirm'),
    path('reset/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),



]