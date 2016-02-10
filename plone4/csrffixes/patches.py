from plone.protect.interfaces import IDisableCSRFProtection
from zope.globalrequest import getRequest
from zope.interface import alsoProvides


def disable_csrf(self, *args, **kwargs):
    alsoProvides(self.request, IDisableCSRFProtection)
    return self._old___call__(*args, **kwargs)


def createScale(self, *args, **kwargs):
    req = getRequest()
    if req:
        alsoProvides(req, IDisableCSRFProtection)
    return self._old_createScale(*args, **kwargs)


def namedfile_scale(self, *args, **kwargs):
    if self.request is not None:
        alsoProvides(self.request, IDisableCSRFProtection)
    return self._old_scale(*args, **kwargs)


def logoutUser(self, *args, **kwargs):
    if len(args) > 0:
        alsoProvides(args[0], IDisableCSRFProtection)
    return self._old_logoutUser(*args, **kwargs)
