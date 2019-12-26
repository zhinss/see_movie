from rest_framework.views import exception_handler as exc_handler
from rest_framework.response import Response
from utils.logging import logger


# 自定义异常函数
def exception_handler(exc, context):
    """自定义异常函数"""
    response = exc_handler(exc, context)

    # 记录错误
    logger.error('%s - %s - %s' % (context['view'], context['request'].method, exc))

    if response is None:
        return Response({'detail': f'{exc}'}, status=500, exception=True)

    return response
