This repository is archived and read only.

If you want to unarchive it, then post to the [Admin & Infrastructure (AI) Team category on the Plone Community Forum](https://community.plone.org/c/aiteam/55).

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

You need to make changes to your buildout configuration, and this differs per Plone version.


Plone 5
-------

This package is not needed.


Plone 4.3.8 and higher
----------------------

::

    eggs =
        ...
        plone4.csrffixes
        ...

    [versions]
    cssselect = 0.9.1
    plone4.csrffixes = 1.1.1
    plone.protect = 3.1.4
    ...


Plone 4.3 - 4.3.7
-----------------

::

    eggs =
        ...
        plone4.csrffixes
        ...

    [versions]
    cssselect = 0.9.1
    plone4.csrffixes = 1.1.1
    plone.keyring = 3.0.1
    plone.locking = 2.0.10
    plone.protect = 3.1.4
    ...


Plone 4.2
---------

::

    eggs =
        ...
        plone4.csrffixes
        ...

    [versions]
    cssselect = 0.9.1
    lxml = 2.3.6
    plone4.csrffixes = 1.1.1
    plone.keyring = 3.0.1
    plone.locking = 2.0.10
    plone.protect = 3.0.26
    ...


Plone 4.0 and 4.1
-----------------

::

    eggs =
        ...
        plone4.csrffixes
        ...

    [versions]
    cssselect = 0.9.1
    lxml = 2.3.6
    plone4.csrffixes = 1.1.1
    plone.keyring = 3.0.1
    plone.locking = 2.0.10
    plone.protect = 3.0.26
    repoze.xmliter = 0.5
    ...


Plone 3
-------

This package is not supported on Plone 3.  Do not use it.


Additional version hints
------------------------

For more version hints in case of possible problems, see https://github.com/plone/plone4.csrffixes/issues/12.
Discussions on `community.plone.org <https://community.plone.org/t/versions-section-for-hotfix20151006-in-plone-4-3-18/7541>`_ can be useful too.


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
