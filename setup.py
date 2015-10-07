from setuptools import setup, find_packages

version = '1.0.3'

setup(name='plone4.csrffixes',
      version=version,
      description="",
      long_description="%s\n\n%s" % (
          open('README.txt').read(),
          open('CHANGES.txt').read()
      ),
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
      ],
      keywords='plone csrf',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/plone4.csrffixes',
      license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone4'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.protect>=3.0.11',
          'plone.keyring>=3.0.1',
          'plone.locking>=2.0.8',
          'collective.monkeypatcher'
      ],
      extras_require={
          'test': ['plone.app.testing'],
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """)
