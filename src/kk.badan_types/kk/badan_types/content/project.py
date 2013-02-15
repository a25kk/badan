"""Definition of the Project content type
"""

from zope.interface import implements

from AccessControl import ClassSecurityInfo
from DateTime import DateTime

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.document import ATDocumentBase
from Products.ATContentTypes.content.image import ATCTImageTransform

from Products.ATContentTypes.configuration import zconf

from Products.validation.config import validation
from Products.validation.validators.SupplValidators import MaxSizeValidator
from Products.validation import V_REQUIRED

from Products.CMFCore.permissions import ModifyPortalContent, View

# -*- Message Factory Imported Here -*-

from kk.badan_types.interfaces import IProject
from kk.badan_types.config import PROJECTNAME
from kk.badan_types import badan_typesMessageFactory as _

ProjectSchema = folder.ATFolderSchema.copy() + atapi.Schema((

       atapi.DateTimeField('ProjectDate',
                  required=True,
                  searchable=False,
                  default_method=DateTime,
                  languageIndependent=True,
                  widget=atapi.CalendarWidget(
                        description='',
                        label=_(u'label_project_date', default=u'Project Date')
                        )),
       atapi.StringField("city", 
       required = False), 
    	atapi.ImageField('image',
        	required=False,
        	storage=atapi.AnnotationStorage(migrate=True),
        	languageIndependent=True,
        	max_size=zconf.ATNewsItem.max_image_dimension,
        	sizes={'large': (768, 768),
               'preview': (400, 400),
               'mini': (200, 200),
               'thumb': (128, 128),
               'tile': (64, 64),
               'icon': (32, 32),
               'listing': (16, 16),
              },
        	validators=(('isNonEmptyFile', V_REQUIRED),
                    ('checkNewsImageMaxSize', V_REQUIRED)),
        	widget=atapi.ImageWidget(
            	description=_(u'help_project_image', default=u'Will be shown in the projects listing.'),
           		label=_(u'label_project_image', default=u'Image'),
            	show_content_type=False)),
    	atapi.TextField('text',
        	required=False,
        	searchable=True,
        	primary=True,
        	storage=atapi.AnnotationStorage(migrate=True),
        	validators=('isTidyHtmlWithCleanup',),
        
        	default_output_type='text/x-html-safe',
        	widget=atapi.RichWidget(
            	description='',
            	label=_(u'label_body_text', u'Body Text'),
            	rows=25,
            	allow_file_upload=zconf.ATDocument.allow_document_upload)),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

ProjectSchema['title'].storage = atapi.AnnotationStorage()
ProjectSchema['description'].storage = atapi.AnnotationStorage()


schemata.finalizeATCTSchema(
    ProjectSchema,
    folderish=True,
    moveDiscussion=False
)


class Project(folder.ATFolder, ATDocumentBase, ATCTImageTransform):
    """Project"""
    implements(IProject)

    meta_type = "Project"
    schema = ProjectSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    security = ClassSecurityInfo()

    security.declareProtected(View, 'tag')
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        if 'title' not in kwargs:
            kwargs['title'] = self.Title()
        return self.getField('image').tag(self, **kwargs)


    def __bobo_traverse__(self, REQUEST, name):
        """Transparent access to image scales
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image

        return ATDocumentBase.__bobo_traverse__(self, REQUEST, name)


atapi.registerType(Project, PROJECTNAME)
