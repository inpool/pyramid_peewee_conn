import os

from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(HERE, 'CHANGES.txt')) as f:
    CHANGES = f.read()

REQUIRES = [
    'pyramid',
    'peewee',
]

DESCRIPTION = (
    'Provides integration between the Pyramid web application and the peewee ORM.'
)
setup(
    name='pyramid_peewee_conn',
    version='0.7.1',
    description=DESCRIPTION,
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python", "Framework :: Pyramid",
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
    install_requires=REQUIRES,
    extras_require={
        'testing': ['pytest'],
    })
