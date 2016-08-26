import random
from django.core.cache import caches
from django.core.mail import mail_admins


class PendingUserStore(object):
    # TODO: Implement in the future key for the tokens
    def __init__(self):

        self.pending = caches['pending']

    def add_by_sessionid(self, request, user):
        """ Put user in the store,
            returns a code
         """
        request.session.cycle_key()
        sessionid = request.session.session_key
        code = random.randint(1000, 9999)
        mail_admins('Verification code', 'Code: {}'.format(code))
        self.pending.set(sessionid, (code, user), 120)
        print(code)
        return code

    def get_by_sessionid(self, sessionid, code):
        """ Get user by sessionid and code"""
        check_code, user = self.pending.get(sessionid)
        if int(code) == check_code:
            return user
        return None
