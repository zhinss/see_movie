import time

from alipay import AliPay
from libs.iPay.settings import *


alipay = AliPay(
    appid=APP_ID,
    app_notify_url=None,  # the default notify path
    app_private_key_string=app_private_key_string,
    # alipay public key, do not use your own public key!
    alipay_public_key_string=alipay_public_key_string,
    sign_type=SIGN,  # RSA or RSA2
    debug=DEBUG  # False by default
)

order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no=time.time(),
    total_amount=0.01,
    subject='冲冲冲',
    return_url="https://example.com",
    notify_url="https://example.com/notify"  # this is optional
)
