from django.utils.translation import ugettext_lazy as _


class FileBrowserImageSize(object):
    """
    Filebrowser Image size. Perhaps needs to be combined with the filebrowser settings for consistency.

    For now see: settings.FILEBROWSER_VERSIONS (keys match constants)
    """

    #Todo: Just a stub, you need to implement this for your site
    ONE_COL = 'one'
    TWO_COL = 'two'
    THREE_COL = 'three'

    PAGE_LARGE = 'page_large'
    PAGE_SMALL = 'page_small'

    SIZES = (
        (ONE_COL, _('One column')),
        (TWO_COL, _('Two columns')),
        (THREE_COL, _('Three columns'))
    )

    @classmethod
    def default(cls):
        return cls.ONE_COL

