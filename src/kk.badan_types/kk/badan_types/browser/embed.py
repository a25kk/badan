from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class EmbedView(BrowserView):
    """ Embed view """
    __call__ = ViewPageTemplateFile('embed.pt')