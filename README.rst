plone4.csrffixes
================

The package aims to backport the auto CSRF implementation from Plone 5
to Plone 4.

The reason this is necessary is because there are a lot of CSRF problem
with the ZMI that Zope2 will never be able to fix.

See https://plone.org/security/hotfix/20151006
for more details.


Installation
============


Plone 4.3, 4.2, 4.1 and 4.0
---------------------------

add `plone4.csrffixes` to eggs list::

    eggs =
        ...
        plone4.csrffixes
        ...


add a new version pin for plone.protect, plone.keyring and plone.locking::

    [versions]
    ...
    plone.keyring = 3.0.1
    plone.locking = 2.0.10
    plone.protect = 3.0.21
    ...


Plone 4.0 and 4.1
-----------------

If lxml is not already included in your site, this package has a dependency
on lxml and will pull it in when installed.

We recommend pinning to version 2.3.6 of lxml. If you use a version of lxml > 3,
you'll need to also install the ``cssselect`` package. Since version
1.0.4 we require ``cssselect`` in our ``setup.py`` so it is
automatically installed.


Additional addon versions
-------------------------

To prevent some write on read errors that might cause false
positives with the auto csrf protection, these version pins have
been reported to work upgrading to::

    Products.CMFQuickInstallerTool = 3.0.12
    Products.PlonePAS = 5.0.4

For more version hints, see https://github.com/plone/plone4.csrffixes/issues/12.


Robot framework
---------------

plone4.csrffixes registers via z3c.autoinclude for Plone instances and is not
loaded in tests.

You need to include plone4.csrffixes in your package configure.zcml for it to
load in your tests::

    <include package="plone4.csrffixes" />


Still needed?
-------------

Most patches in this package have been ported to their original location.
If you use Plone 4.3.8 or later, then it is sufficient to add ``plone.protect 3.0.21`` or higher.
With those versions, you may not need ``plone4.csrffixes`` anymore.

But adding ``plone4.csrffixes`` may still help avoid a few confirmation pages, because it has this code which is extra:

- It checks the referer.  If the previous page is within the Plone Site, no cross site checks are done.

- If the current page is a ZMI page (Zope Management Interface) all links are rewritten to have a CSRF token.

- Several other links get the CSRF token appended, for example in the Actions dropdown (Copy, Delete, etcetera).

This extra code basically has no influence on the csrf checks.
But it allows some write-on-reads: situations where simply viewing a page, without submitting a form, already makes a change in the database.
A write-on-read is not wanted, but on Plone 4 it cannot always be avoided.
Some core code and also add-ons may do this.

So the advice is:

1. Try Plone 4.3.8 or higher with ``plone.protect`` 3.0.21 or higher *without* ``plone4.csrffixes``.

2. If that gives too many needless confirmation pages, then add ``plone4.csrffixes`` again.
