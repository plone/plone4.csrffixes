from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides


def disable_csrf(self, *args, **kwargs):
    alsoProvides(self.request, IDisableCSRFProtection)
    return self._old___call__(*args, **kwargs)