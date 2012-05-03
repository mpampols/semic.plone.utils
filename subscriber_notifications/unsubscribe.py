# In this example, the subscribed object must have a field with a list of subscribed people (getSubscribers)
# See: sendEmail on send_email.py

def do_unsubscribe(self,object_id,email,s):

    import sha

    from Products.PythonScripts.standard import html_quote
    from Products.CMFCore.utils import getToolByName

    plone_utils = getToolByName(self, 'plone_utils', None)
    workflowTool = getToolByName(self, "portal_workflow")

    urltool = getToolByName(self, 'portal_url')
    section_path = urltool.getPortalPath()+ '/'

    # Search the object where user is subscribed to
    obj_query = self.portal_catalog({'meta_type':{'query':['Content Type']},
                                     'review_state':'published',
                                     'id':object_id
                                   })[:1]

    obj_to_unsubscribe = obj_query.getObject()

    if (obj_to_unsubscribe):
        actual_subscribers = list(obj_to_unsubscribe.getSubscribers())
        if email in actual_subscribers:
            string_secret = "<YOUR SECRET RANDOM STRING>"
            subscription_secret = sha.new(email + obj_to_unsubscribe.getId() + string_secret).hexdigest()

            # Check if the secret is correct, then we can unsubscribe the user from our field list
            # "s" is the secret we receive from the email URL
            if (subscription_secret == s):
                if (email in actual_subscribers):
                    actual_subscribers.remove(email)
                    new_subscribers_tuple = tuple(actual_subscribers)
                    obj_oposicion.setSubscribers(new_subscribers_tuple)
                    obj_oposicion.reindexObject()
                    message = 'Successfully unsubscribed from this object.'
                else:
                    message = 'You are no longer subscribed.'
    else:
        # Object doesn't exist
        message = 'The object you want to unsubscribe no longer exists.'

    return message