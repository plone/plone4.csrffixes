Changelog
=========

1.1.1 (unreleased)
------------------

Breaking changes:

- *add item here*

New features:

- *add item here*

Bug fixes:

- Updated documentation on versions and on the necessity of this package.  [maurits]


1.1 (2016-08-26)
----------------

New features:

- Depend on ``plone.protect 3.0.19`` or higher.  This adds
  ``protect.js``, so we do not have to do this anymore.  See issue
  https://github.com/plone/plone.protect/issues/42
  [maurits]

- Factor out referrer/origin backstop into its own method so it can be
  customized on a subclassed transform.
  [lgraf]

Bug fixes:

- Change extension of CHANGES and README from txt to rst.
  [gforcada]

- include a setup.cfg and a .editorconfig file with code conventions:
  - settings for isort
  - plone styleguide settings
  [loechel]

- apply code conventions [loechel]


1.0.9 (2015-11-18)
------------------

- fix potential issues with tinymce patch
  [vangheem]

- Add documentation for loading plone4.csrffixes for robot framework testing
  [lbrannon]


1.0.8 (2015-10-30)
------------------

- Fix issue where redirects would contain an unparsable response
  [vangheem]

- make plone lock operations safe
  [vangheem]

- Check options before trying to work on them
  [ale-rt]

- Use "application/javascript" media type instead of the obsolete "text/javascript".
  [hvelarde]


1.0.7 (unreleased)
------------------

- Skipped by mistake.


1.0.6 (2015-10-12)
------------------

- add a trailing slash on the site referrer matching
  [vangheem]


1.0.5 (2015-10-08)
------------------

- Handle TypeError caused by getToolByName on an
  invalid context
  [vangheem]


1.0.4 (2015-10-07)
------------------

- add cssselect dependency for people who install lxml > 3
  by mistake on Plone 4.0 and 4.1
  [vangheem]

1.0.3 (2015-10-07)
------------------

- prevent TypeError from occurring when checking commit of
  non-string keys on an OOBTree instance. Fixes #5
  [vangheem]

- Check to see if tinymce ajax is already patched or not.
  This prevents JavaScript recursion error.
  [awello, cekk]


1.0.2 (2015-10-06)
------------------

- use a better guess at if we should rewrite urls
  for zmi
  [vangheem]


1.0.1 (2015-10-06)
------------------

- correctly check for origin header
  [vangheem]

1.0.0 (2015-10-06)
------------------

- initial release
