import xadmin
from movie import models


xadmin.site.register(models.Movie)
xadmin.site.register(models.Tag)
xadmin.site.register(models.Tag2Movie)
xadmin.site.register(models.Performer)
xadmin.site.register(models.Per2Movie)
xadmin.site.register(models.Lines)
