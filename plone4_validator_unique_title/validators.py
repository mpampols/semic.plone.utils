from zope.component import adapts
from Products.Archetypes.interfaces import IObjectPostValidation
from Products.PythonScripts.standard import html_quote
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from aeau.contenttypes import contenttypesMessageFactory as _
from aeau.contenttypes.interfaces import ISoci

from Acquisition import aq_inner
from Acquisition import aq_parent

class ValidateUniqueTitle(object):
    """
    Checks if there's an object with the same title inside the folder where the new item it's being created.
    In this example i'm using my own content type: aeau.contenttypes.soci
    """

    implements(IObjectPostValidation)
    adapts(ISoci)

    # Name of the field in which the validator will be applied
    field_name = 'title'

    def __init__(self, context):
        self.context = context

    def __call__(self, request):
        value = request.form.get(self.field_name, request.get(self.field_name, None))

        if value is not None:
            messages = IStatusMessage(request)
            catalog = getToolByName(self.context, "portal_catalog")
            plone_utils = getToolByName(self.context, 'plone_utils', None)

            parent = aq_parent(aq_inner(self.context))

            # Get the object metatype that we are going to create
            object_type = self.context.Type()

            # Actual folder where the object is going to be created, ignoring the portal_factory check
            object_folder = str('/'.join(parent.getPhysicalPath()))
            object_folder = object_folder.replace('/portal_factory/'+object_type,'')

            results = self.context.portal_catalog.searchResults(portal_type=object_type,
                                                                path={'query':object_folder,'level':0,'depth':1},
                                                                Title=value)

            for result in results:
                if self.context.UID() == result.getObject().UID():
                    return None

            if results:
                messages.addStatusMessage(_(u'There is an object in this folder with the same type and title'), type="error")
                return { self.field_name: '' }

        # Returning None means no error
        return None