# This function can be used to send a notification email when a object state changes.
# It also creates a specific user hash that can be used to unsubscribe from this notifications
# See: do_unsubscribe on unsubscribe.py

def sendEmail(self,state_change):

    import sha

    obj = state_change.object
    mship = self.portal_membership
    mhost = self.MailHost
    adminEmail = self.email_from_address
    administratorEmailAddress = 'put_yout@email.here'

    # Get a list of subscribers on this particular object
    subscribers = obj.getSubscribers()

    for subscriber in subscribers:

        to_string = subscriber

        message = """
        From: %s
        To: %s
        Subject: <SUBJECT LINE>

        <EMAIL TEXT CONTENT>

        --
        To unsubscribe from this notification, click here:
        http://<URL>/unsubscribe?op=%s&email=%s&s=%s
        """

        string_secret = "<YOUR SECRET RANDOM STRING>"
        mail_secret   = sha.new(to_string + obj.getId() + string_secret).hexdigest()

        msg = message % (
            administratorEmailAddress,
            to_string,
            obj.absolute_url(),
            obj.getId(),
            to_string,
            mail_secret
        )

        mh = self.MailHost
        mh.send(msg,
                mto=to_string,
                mfrom=administratorEmailAddress,
                subject="<SUBJECT LINE>")

        print "Notification sent."

    return True