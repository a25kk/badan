from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from OFS.interfaces import IOrderedContainer
from collective.flowplayer.interfaces import IVideo, IAudio
def get_position_in_parent(obj):
    """
    Use IOrderedContainer interface to extract the object's manual ordering position
    """
    parent = obj.aq_inner.aq_parent
    ordered = IOrderedContainer(parent, None)
    if ordered is not None:
        return ordered.getObjectPosition(obj.getId())
    return 0
    
def sort_by_position(a, b):
    """
    Python list sorter cmp() using position in parent.

    Descending order.
    """
    return get_position_in_parent(a) - get_position_in_parent(b)
    
class ProjectView(BrowserView):
    """ Project view """
    __call__ = ViewPageTemplateFile('project.pt')
    
    
    def gallery(self):
        queried_objects = list(self.context.listFolderContents())
        queried_objects = sorted(queried_objects, sort_by_position)
        result = {'gallery':[],'sound':[]}
        for obj in queried_objects:
            ptype = obj.portal_type
            if ptype == 'Image' or (ptype == 'Embed media' and obj.getMediaType() == '0') or (ptype in ['File', 'Link'] and IVideo.providedBy(obj)):
                result['gallery'].append(obj)
            if (ptype == 'Embed media' and obj.getMediaType() == '1') or (ptype in ['File', 'Link'] and IAudio.providedBy(obj)) :
                result['sound'].append(obj)
        return result
    
    def projects(self):
        parent = self.context.aq_parent
        results = self.context.portal_catalog(portal_type="Project", sort_on = "getObjPositionInParent", path = {'query':'/'.join(parent.getPhysicalPath()), 'depth':1})
        res = []
        for result in results:
            if result.UID != self.context.UID():
                res.append(result)
            
        
        return res

