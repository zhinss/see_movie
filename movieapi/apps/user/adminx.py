# xadmin全局配置
import xadmin
from xadmin import views
from user import models


class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "看·电影"  # 设置站点标题
    site_footer = "看·电影有限公司"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠


xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(models.Favorite)
xadmin.site.register(models.UpOrDown)
xadmin.site.register(models.Comment)
xadmin.site.register(models.LinesComment)
