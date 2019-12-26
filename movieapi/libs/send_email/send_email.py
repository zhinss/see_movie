# Django内置的邮箱发送函数
from django.core.mail import send_mail
from settings.dev import EMAIL_FROM


# 发送邮件
def send_email(email, username):
    """发送邮件"""
    email_title = '看·电影重置密码'
    email_body = f'亲爱的用户{username}, 您的密码已重置为{username}123,请不要向任何人透露。' \
                 f'' \
                 f'点击链接http://127.0.0.1:8080/#/login 重新登陆'

    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

    # 如果发送成功
    if send_status:
        pass

