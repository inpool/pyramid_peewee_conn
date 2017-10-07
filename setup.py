import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'peewee',
]


setup(name='Starter',
      version='0.5',
      description='A package which provides integration between the Pyramid web application server and the peewee ORM. ',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
          "Topic :: Database"
      ],
      author='Inpool',
      author_email='inpool@126.com',
      url='https://github.com/inpool/pyramid_peewee_conn',
      keywords='web pyramid peewee',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      )
