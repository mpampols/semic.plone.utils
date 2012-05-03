# -*- coding: utf-8 -*-
import datetime
import urllib

from Acquisition import aq_inner

from zope import interface
from zope import schema

from zope.app.pagetemplate import viewpagetemplatefile
from zope.app.component.hooks import getSite

from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.statusmessages.interfaces import IStatusMessage

# Control BadRequest errors (duplicate id's found)
try: from zExceptions import BadRequest
except ImportError: BadRequest = 'BadRequest'

# Control errors caused by WebDAV open objects in Plone durint import
from Products.CMFDefault.exceptions import ResourceLockedError

import StringIO
import csv

class Import(BrowserView):

    # Template where we show the import results
    template = viewpagetemplatefile.ViewPageTemplateFile('import.pt')

    # Import function
    def render(self):
        plone_utils = getToolByName(self.context, 'plone_utils')
        workflowTool = getToolByName(self.context, "portal_workflow")

        # Read the CSV file
        csv_contents = str(self.context)
        f = StringIO.StringIO(csv_contents)
        file = f.read()
        csv_reader = csv.reader(file.splitlines(), delimiter=';')

        # Counting successful and failed register imports
        stats_ok = 0
        stats_failed = 0

        # Set the name of the content type to create
        content_type = "Name of the Content Type"

        headers = 0
        for field in csv_reader:
            if (headers == 1):
               
                # Set the csv values to new python variables and do the proper processing for each register
                obj_id          = plone_utils.normalizeString(unicode(field[0]))
                obj_title       = str(field[1])
                obj_descripcion = str(field[2])
                
                # Try to create the object in Plone
                try:
                    subfolder_item[1].invokeFactory(content_type, obj_id)
                    obj_newObject = getattr(self, obj_id)
                    obj_newObject.setTitle(obj_title)
                    obj_newObject.setDescription(obj_description)
                    obj_newObject.reindexObject()
                    stats_ok += 1

                    except BadRequest:
                        print "Can't create object."
                        stats_failed += 1

                    except ResourceLockedError:
                        print "Can't create object, locked entry by WebDAV."
                        stats_failed += 1

            if (headers == 0):
                headers = 1

        return str("Import process results: CREATED: " + str(stats_ok) + " FAILED: " + str(stats_failed))

    def __call__(self):
        return self.render()