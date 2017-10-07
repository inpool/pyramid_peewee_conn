Pyramid_peewee_conn README
==========================

Overview
---------------

A package which provides integration between the Pyramid web application server and 
the peewee ORM.

It's tested under CPython 3.4 but maybe run under any environ which pyramid and peewee can be used.
If you found any issue in using it, please [submit it](https://github.com/inpool/pyramid_peewee_conn/issues).

Installation
------------

Install using setuptools, e.g. (within a virtual environment)::

  $ easy_install pyramid_peewee_conn

Setup
-----

Once ``pyramid_peewee_conn`` is installed, you must use the ``config.include``
mechanism to include it into your Pyramid project's configuration.  In your
Pyramid project's ``__init__.py``:

.. code-block:: python
   :linenos:

   config = Configurator(.....)
   config.include('pyramid_peewee_conn')

Alternately you can use the ``pyramid.includes`` configuration value in your
``.ini`` file:

.. code-block:: ini
   :linenos:

   [app:myapp]
   pyramid.includes = pyramid_peewee_conn

Using
-----

For :mod:`pyramid_peewee_conn` to work properly, you must add at least one
setting to your of your Pyramid's ``.ini`` file configuration (or to the
``settings`` dictionary if you're not using ini configuration):
``peewee.urls``.  For example:

.. code-block:: ini

   [app:myapp]
   ...
   peewee.url = postgres://username:password@hostname:port/database_name
   ...

The ``peewee.url`` parameter is a URL defined in the peewee documentation
[Connecting using a Database URL](https://peewee.readthedocs.org/en/latest/peewee/database.html#connecting-using-a-database-url)

Once you've both included the ``pyramid_peewee_conn`` into your configuration
via ``config.include('pyramid_zodbconn')`` and you've added a
``peewee.url`` setting to your configuration, you can then use the
:func:`pyramid_peewee_conn.get_db` API in your Pyramid application, most
commonly in a model defintion:

.. code-block:: python
   :linenos:

    from peewee import *
    from pyramid_peewee_conn import get_db
    
    db = get_db()

    class Person(Model):
        name = CharField()
        age = IntegerField()

        class Meta:
            database = db

    class Pet(Model)
        name = CharField()
        owner = ForeignKeyField(Person, related_name='pets')
        animal_type = CharField()

    db.connect()
    db.create_tables([Person, Pet])

The :func:`pyramid_peewee_conn.get_db` API returns a peewee.Database instance which 
you've specified via ``peewee.url`` in your configuration.

Named Databases
---------------

If you need to use more than one database in your Pyramid application,
you can use *named* databases via configuration.  Named databases are
specified by ``zodbconn.uri.thename`` in settings configuration.  For
example:

.. code-block:: ini

   [app:myapp]
   ...
   peewee.url = postgres://username:password@hostname:port/database_name
   peewee.url.memory = sqlite:///:memory:
   ...

Once this is done, you can use :func:`pyramid_peewee_conn.get_db` to
obtain a reference to each of the named databases:

.. code-block:: python

    db = get_db() # main database
    memory_db = get_db('memory')

The ``peewee.url.memory`` parameter example above is a URL which
describes peewee database, in the same format as ``peewee.url``.  You can
combine named and unnamed database configuration in the same application.
You can also use named databases without a main database.

Another config format
----------------------

Perhaps you had used pyramid_peewee, which config ``peewee.urls`` in the ini configure file like this:

.. code-block:: ini

    [app:myapp]
    ...
    peewee.urls = postgres://username:password@hostname:port/database_1
        sqlite:///test.db
    ...

This config format is supported. In this case, the database name is the database name.
The prior configuration is equal to the next:

.. code-block:: ini

    [app:myapp]
    ...
    peewee.url = postgres://username:password@hostname:port/database_1
    peewee.url.database_1 = postgres://username:password@hostname:port/database_1
    peewee.url.test.db = sqlite:///test.db
    ...

Conflict
----------

Once there are both two format configure and have some database conflict, 
the explicit configuration will be used.

.. code-block:: ini

    [app:myapp]
    ...
    peewee.url = postgres://user:pass@host:port/database
    peewee.url.db1 = mysql://user:pass@host:port/database
    peewee.urls = 
        mysql://user:pass@host:port/db1
        postgres://user:pass@host:port/database
    ...

The prior configuration is equal next:

.. code-block:: ini

    [app:myapp]
    ...
    peewee.url = postgres://user:pass@host:port/database
    peewee.url.db1 = mysql://user:pass@host:port/database
    peewee.url.database = postgres://user:pass@host:port/database
    ...