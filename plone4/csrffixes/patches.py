from zope.globalrequest import getRequest
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides


def disable_csrf(self, *args, **kwargs):
    alsoProvides(self.request, IDisableCSRFProtection)
    return self._old___call__(*args, **kwargs)


def createScale(self, *args, **kwargs):
    req = getRequest()
    if req:
        alsoProvides(req, IDisableCSRFProtection)
    return self._old_createScale(*args, **kwargs)