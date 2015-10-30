import logging

from AccessControl import getSecurityManager
from BTrees.OOBTree import OOBTree
from Products.CMFCore.utils import getToolByName
from lxml import etree
from plone.app.blob.content import ATBlob
from plone.keyring.interfaces import IKeyManager
from plone.protect.authenticator import createToken
from plone.protect.authenticator import isAnonymousUser
from plone.protect.auto import CSRF_DISABLED
from plone.protect.auto import ProtectTransform
from plone.protect.auto import safeWrite
from plone.protect.interfaces import IConfirmView
from plone.protect.interfaces import IDisableCSRFProtection
from plone.protect.utils import addTokenToUrl
from plone.protect.utils import getRoot
from plone.protect.utils import getRootKeyManager
from plone.transformchain.interfaces import ITransform
from zope.component import ComponentLookupError
from zope.component import adapts
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.interface import implements, Interface

try:
    from zope.component.hooks import getSite
except:
    from zope.app.component.hooks import getSite


LOGGER = logging.getLogger('plone.protect')

_add_rule_token_selector = ','.join([
    '#rules_table_form a',
    '.contentViews li a,.contentActions li a',
    '#portal-column-one ul.configlets a',
    '.portletAssignments a'
])

class Protect4Transform(ProtectTransform):
    """
    Additional plone.protect transforms to fix zmi issues
    """
    implements(ITransform)
    adapts(Interface, Interface)  # any context, any request

    # should run JUST before plone.protect transform
    order = 8889

    site = None
    key_manager = None
    safe_views = (
        'plone_lock_operations',
    )

    def transformBytes(self, result, encoding):
        result = unicode(result, encoding, 'ignore')
        return self.transformIterable(result, encoding)

    def transformString(self, result, encoding):
        return self.transformIterable(result, encoding)

    def transformUnicode(self, result, encoding):
        return self.transformIterable(result, encoding)

    def transformIterable(self, result, encoding):
        if CSRF_DISABLED:
            return

        # only auto CSRF protect authenticated users
        if isAnonymousUser(getSecurityManager().getUser()):
            return

        # if on confirm view, do not check, just abort and
        # immediately transform without csrf checking again
        if IConfirmView.providedBy(self.request.get('PUBLISHED')):
            return

        # next, check if we're a resource not connected
        # to a ZODB object--no context
        context = self.getContext()
        if not context:
            return

        try:
            tool = getToolByName(context, 'portal_url', None)
            if tool:
                self.site = tool.getPortalObject()
        except TypeError:
            self.site = getSite()

        try:
            self.key_manager = getUtility(IKeyManager)
        except ComponentLookupError:
            root = getRoot(context)
            self.key_manager = getRootKeyManager(root)

        if self.site is None and self.key_manager is None:
                # key manager not installed and no site object.
                # key manager must not be installed on site root, ignore
                return

        return self.transform(result, encoding)

    def getViewName(self):
        try:
            return self.getContext().__name__
        except AttributeError:
            return None

    def transform(self, result, encoding):

        site_url = 'foobar'
        if self.site:
            site_url = self.site.absolute_url()

        registered = self._registered_objects()
        if len(registered) > 0 and \
                not IDisableCSRFProtection.providedBy(self.request):
            if self.getViewName() in self.safe_views:
                alsoProvides(self.request, IDisableCSRFProtection)
            else:
                # in plone 4, we need to do some more trickery to
                # prevent write on read errors
                annotation_keys = (
                    'plone.contentrules.localassignments',
                    'syndication_settings',
                    'plone.portlets.contextassignments')
                for obj in registered:
                    if isinstance(obj, OOBTree):
                        safe = False
                        for key in annotation_keys:
                            try:
                                if key in obj:
                                    safe = True
                                    break
                            except TypeError:
                                pass
                        if safe:
                            safeWrite(obj)
                    elif isinstance(obj, ATBlob):
                        # writing scales is fine
                        safeWrite(obj)

                # check referrer/origin header as a backstop to check
                # against false positives for write on read errors
                referrer = self.request.environ.get('HTTP_REFERER')
                if referrer:
                    if referrer.startswith(site_url + '/'):
                        alsoProvides(self.request, IDisableCSRFProtection)
                else:
                    origin = self.request.environ.get('HTTP_ORIGIN')
                    if origin and origin == site_url:
                        alsoProvides(self.request, IDisableCSRFProtection)

        result = self.parseTree(result, encoding)
        if result is None:
            return None

        try:
            root = result.tree.getroot()
        except AttributeError:
            # odd case here on redirects still containing a response
            # object
            return

        try:
            token = createToken(manager=self.key_manager)
        except ComponentLookupError:
            return

        if self.site is not None:
            body = root.cssselect('body')[0]
            protect_script = etree.Element("script")
            protect_script.attrib.update({
                'type': "application/javascript",
                'src': "%s/++resource++protect.js" % site_url,
                'data-site-url': site_url,
                'data-token': token,
                'id': 'protect-script'
            })
            body.append(protect_script)

        # guess zmi, if it is, rewrite all links
        last_path = self.request.URL.split('/')[-1]
        if last_path == 'manage' or last_path.startswith('manage_'):
            root.make_links_absolute(self.request.URL)
            def rewrite_func(url):
                return addTokenToUrl(
                    url, self.request, manager=self.key_manager)
            root.rewrite_links(rewrite_func)

        # Links to add token to so we don't trigger the csrf
        # warnings
        for anchor in root.cssselect(_add_rule_token_selector):
            url = anchor.attrib.get('href')
            # addTokenToUrl only converts urls on the same site
            anchor.attrib['href'] = addTokenToUrl(
                url, self.request, manager=self.key_manager)

        return result
