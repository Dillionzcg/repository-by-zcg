from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('verify-email/<int:user_id>/', views.verify_email_view, name='verify_email'),
    path('resend-code/<int:user_id>/', views.resend_verification_code, name='resend_code'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]