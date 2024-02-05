from views.user.gists import View as _View
from ..mixins import DownloadMixin

class View(DownloadMixin,_View):
    pass
