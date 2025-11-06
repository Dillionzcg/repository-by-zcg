from django.core.mail import send_mail
from django.conf import settings
from .models import EmailVerification


def send_verification_email(user):
    # 删除旧的验证码
    EmailVerification.objects.filter(user=user).delete()

    # 生成新的验证码
    code = EmailVerification.generate_code()
    verification = EmailVerification.objects.create(user=user, code=code)

    # 发送邮件
    subject = '邮箱验证码'
    message = f'您的验证码是: {code}，有效期为10分钟。'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    return verification