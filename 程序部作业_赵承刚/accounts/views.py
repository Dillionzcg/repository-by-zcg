from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm, EmailVerificationForm
from .models import CustomUser, EmailVerification
from .utils import send_verification_email


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # 方案2：临时跳过邮箱验证
            user.email_verified = True  # 直接标记为已验证
            user.save()
            login(request, user)  # 直接登录
            messages.success(request, '注册成功！')
            return redirect('home')


    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def verify_email_view(request, user_id):
    user = CustomUser.objects.get(id=user_id)

    if request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                verification = EmailVerification.objects.get(user=user, code=code)
                if not verification.is_expired():
                    user.email_verified = True
                    user.save()
                    verification.delete()
                    messages.success(request, '邮箱验证成功！您现在可以登录了。')
                    return redirect('login')
                else:
                    messages.error(request, '验证码已过期，请重新获取。')
            except EmailVerification.DoesNotExist:
                messages.error(request, '验证码错误，请重新输入。')
    else:
        form = EmailVerificationForm()

    return render(request, 'verification.html', {'form': form, 'user': user})


def resend_verification_code(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    send_verification_email(user)
    messages.success(request, '验证码已重新发送！')
    return redirect('verify_email', user_id=user.id)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.email_verified:
                    login(request, user)
                    messages.success(request, f'欢迎回来，{username}！')
                    return redirect('home')
                else:
                    messages.error(request, '请先验证您的邮箱。')
                    return redirect('verify_email', user_id=user.id)
            else:
                messages.error(request, '用户名或密码错误。')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


#@login_required
def logout_view(request):
    logout(request)
    messages.success(request, '您已成功退出登录。')
    return redirect('login')


@login_required
def home_view(request):
    return render(request, 'index.html')