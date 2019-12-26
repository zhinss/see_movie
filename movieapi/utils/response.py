from rest_framework.response import Response


# 自定义APIResponse返回类
class APIResponse(Response):
    """自定义APIResponse返回类"""
    def __init__(self, data_status=0, data_msg='ok', results=None,
                 status=None, template_name=None, headers=None,
                 exception=False, content_type=None):

        data = {
            'status': data_status,
            'msg': data_msg,
        }

        if results is not None:
            data['results'] = results

        super().__init__(data=data, status=status,
                         template_name=template_name, headers=headers,
                         exception=exception, content_type=content_type)

