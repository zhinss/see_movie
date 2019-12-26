# 轮播图显示数
BANNER_NUM = 4

# 验证码过期时间(秒)
CODE_TIME = 300000

# 短信缓存的key
SMS_CACHE_KEY = 'sms_%s'

# 验证码长度
CODE_LEN = 6

# 上线后必须换成公网地址
# 根路径
# BASE_URL = 'http://127.0.0.1:8000'
BASE_URL = 'http://106.15.226.52:8000'

# 前台http根路径
# MOVIE_URL = 'http://127.0.0.1:8080'
MOVIE_URL = 'http://106.15.226.52:80'

# 订单支付成功的后台异步回调接口
NOTIFY_URL = BASE_URL + '/order/success'

# 订单支付成功的前台同步回调接口
RETURN_URL = MOVIE_URL + '/pay/success'
