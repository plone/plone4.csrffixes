import logging

from AccessControl import getSecurityManager
from plone.keyring.interfaces import IKeyManager
from plone.protect.authenticator import createToken
from plone.protect.authenticator import isAnonymousUser
from plone.protect.auto import CSRF_DISABLED
from plone.protect.auto import ProtectTransform
from plone.protect.interfaces import IConfirmView
from plone.transformchain.interfaces import ITransform
from zope.component import ComponentLookupError
from zope.component import adapts
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.interface import implements, Interface
from lxml import etree
from plone.protect.auto import safeWrite
from BTrees.OOBTree import OOBTree
from plone.protect.interfaces import IDisableCSRFProtection
from plone.protect.utils import addTokenToUrl
from plone.app.blob.content import ATBlob


LOGGER = logging.getLogger('plone.protect')


PROTECT_AJAX = """
if(jQuery){
    var base_url = "%s";
    var token = "%s";
    jQuery.ajaxSetup({
        beforeSend: function (xhr, options){
        debugger;
            if(!options.url){
                return;
            }
            if(options.url.indexOf('_authenticator') !== -1){
                return;
            }
            if(options.url.indexOf(base_url) === 0){
                // only urls that start with the site url
                xhr.setRequestHeader("X-CSRF-TOKEN", token);
            }
        }
    });
}
"""


class Protect4Transform(ProtectTransform):
    """
    Additional plone.protect transforms to fix zmi issues
    """
    implements(ITransform)
    adapts(Interface, Interface)  # any context, any request

    # should be last lxml related transform
    order = 8889

    site = None
    key_manager = None

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

        self.site = getSite()
        try:
            self.key_manager = getUtility(IKeyManager)
        except ComponentLookupError:
            pass

        if self.site is None and self.key_manager is None:
            # key manager not installed and no site object.
            # key manager must not be installed on site root, ignore
            return

        return self.transform(result)

    def transform(self, result):
        result = self.parseTree(result)
        if result is None:
            return None

        root = result.tree.getroot()
        try:
            token = createToken()
        except ComponentLookupError:
            if self.site is None:
                # skip here, utility not installed yet on zope root
                return
            raise

        registered = self._registered_objects()
        if len(registered) > 0 and \
                not IDisableCSRFProtection.providedBy(self.request):
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
                        if key in obj:
                            safe = True
                            break
                    if safe:
                        safeWrite(obj)
                elif isinstance(obj, ATBlob):
                    # writing scales is fine
                    safeWrite(obj)

        body = root.cssselect('body')[0]
        protect_script = etree.Element("script")
        protect_script.attrib['type'] = "text/javascript"
        protect_script.text = PROTECT_AJAX % (
            self.site.absolute_url(),
            token)
        body.append(protect_script)

        # guess zmi, if it is, rewrite all links
        if self.request.URL.split('/')[-1].startswith('manage'):
            root.make_links_absolute(self.request.URL)
            def rewrite_func(url):
                return addTokenToUrl(url)
            root.rewrite_links(rewrite_func)

        # Links to add token to so we don't trigger the csrf
        # warnings
        for anchor in root.cssselect('#edit-bar a'):
            url = anchor.attrib.get('href')
            # addTokenToUrl only converts urls on the same site
            anchor.attrib['href'] = addTokenToUrl(url, self.request)

        return result
