"""Definition of the Embed media content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from kk.badan_types.interfaces import IEmbedmedia
from kk.badan_types.config import PROJECTNAME
from kk.badan_types import badan_typesMessageFactory as _

EmbedmediaSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    	atapi.TextField('code',
        	required=True,
        	searchable=False,
        	primary=True,
        	storage=atapi.AnnotationStorage(migrate=True), 
        	default_output_type='text/x-html-safe',
        	widget=atapi.TextAreaWidget(
            	description='',
            	label=_(u'label_embed_code', u'Embed Code'),
            	rows=5)),
    	atapi.StringField('MediaType',
        	required=True,
        	searchable=False,
        	vocabulary = (('0', 'Video'), ('1', 'Audio')),
        	storage=atapi.AnnotationStorage(migrate=True),
        	widget=atapi.SelectionWidget(
            	description='',
            	label=_(u'label_media_type', u'Media Type'),
            	rows=5)),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

EmbedmediaSchema['title'].storage = atapi.AnnotationStorage()
EmbedmediaSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(EmbedmediaSchema, moveDiscussion=False)


class Embedmedia(base.ATCTContent):
    """Embed media"""
    implements(IEmbedmedia)

    meta_type = "Embedmedia"
    schema = EmbedmediaSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Embedmedia, PROJECTNAME)
