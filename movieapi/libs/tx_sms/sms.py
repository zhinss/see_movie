# sms.py
import random

from qcloudsms_py import SmsSingleSender
from django.conf import settings as django_set

from . import settings
from utils.logging import logger

sender = SmsSingleSender(settings.APP_ID, settings.APP_KEY)


# 生成验证码
def get_code(num=django_set.CODE_LEN):
    """生成验证码"""
    code = ''
    for i in range(num):
        code += str(random.randint(0, 9))

    return code


# 发送验证码 需要手机号、验证码、过期时间(min)
def send_sms(mobile, code, exp):
    try:
        response = sender.send_with_param(
            86,
            mobile,
            settings.TEMPLATE_ID,
            params=(code, exp),
            sign=settings.SMS_SIGN,
            extend="", ext="")
        if response and response.get('result') == 0:
            return True
        msg = response.get('result')  # 失败的状态码
    except Exception as msg:
        pass
    logger.error('短信发送失败: %s' % msg)
    return False
