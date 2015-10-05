plone4.csrffixes
================

The package aims to backport the auto CSRF implementation from Plone 5
to Plone 4.

The reason this is necessary is because there are a lot of CSRF problem
with the ZMI that Zope2 will never be able to fix.

Since the auto CSRF protection is overly aggressive, some tricky things
need to be done in order to apply this patch without any false positives.
I'm sure we'll miss things that need to continually be fixed.


Installation
============


Plone 4.3, 4.2 and 4.1
----------------------

add `plone4.csrffixes` to eggs list::

    eggs =
        ...
        plone4.csrffixes
        ...


add a new version pin for plone.protect and plone.keyring::

    [versions]
    ...
    plone.protect = 3.0.9
    plone.keyring = 3.0.1
    plone.locking = 2.0.8
    ...
