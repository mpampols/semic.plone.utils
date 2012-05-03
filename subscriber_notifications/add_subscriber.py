# Add a subscriber email to Plone object with Subscribers field

def add_subscriber(self,plone_object,email):

    from Products.PythonScripts.standard import html_quote
    from Products.CMFCore.utils import getToolByName

    plone_utils = getToolByName(self, 'plone_utils', None)
    workflowTool = getToolByName(self, "portal_workflow")

    urltool = getToolByName(self, 'portal_url')
    section_path = urltool.getPortalPath()+ '/'

    obj_query = self.portal_catalog({'meta_type':{'query':['Content Type']},
                                     'review_state':'published',
                                     'id':object_id
                                   })[:1]

    obj_to_subscribe = obj_query.getObject()

    actual_subscribers = list(obj_to_subscribe.getSubscribers())

    if validateEmail(email):
        if email in actual_subscribers:
            message = "Email alreaxy exists."
        else:
            new_subscribers       = actual_subscribers.append(email)
            new_subscribers_tuple = tuple(actual_subscribers)
            obj_to_subscribe.setSubscribers(new_subscribers_tuple)
            obj_to_subscribe.reindexObject()
            message = "Subscriber added to list"
    else:
        message = "Invalid Email."

    return message

def validateEmail(email):
    import re
    if email==None: return False
    return re.match(r"^[a-zA-Z0-9._%-+]+\@[a-zA-Z0-9._%-]+\.[a-zA-Z]{2,}$", email)!=None