from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase


class BadanKeywordsViewlet(ViewletBase):
    render = ViewPageTemplateFile('keywords.pt')
