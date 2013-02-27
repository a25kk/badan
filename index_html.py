# Example code:

results = context.portal_catalog(portal_type="Project", path = {'query':'/'.join(context.getPhysicalPath()), 'depth':1}, sort_on='getObjPositionInParent')
if len(results):
    obj = results[0].getObject()
    container.REQUEST.RESPONSE.redirect(obj.absolute_url())
else:
    container.REQUEST.RESPONSE.redirect(context.absolute_url() + '/folder_listing')
