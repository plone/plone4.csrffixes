plone4.csrffixes
================

The package aims to backport the auto CSRF implementation from Plone 5
to Plone 4.

The reason this is necessary is because there are a lot of CSRF problem
with the ZMI that Zope2 will never be able to fix.

Since the auto CSRF protection is overly aggressive, some tricky things
need to be done in order to apply this patch without any false positives.
I'm sure we'll miss things that need to continually be fixed.
