==========================
Pyramid_peewee_conn README
==========================

Overview
==========

A package which provides integration between the Pyramid web application server and 
the peewee ORM.

It's tested under CPython 3.4 but maybe run under any environ which pyramid and peewee can be used.
If you found any issue in using it, please `submit it <https://github.com/inpool/pyramid_peewee_conn/issues>`_.

Installation
============

Install using setuptools, e.g. (within a virtual environment)::

  $ easy_install pyramid_peewee_conn

Or using pip::

    $ pip install pyramid_peewee_conn

Or install from github::

    $ git clone https://github.com/inpool/pyramid_peewee_conn
    $ cd pyramid_peewee_conn
    $ python setup.py install

Or if your computer hasn't git command, you can install it via from github::

    $ pip install https://github.com/inpool/pyramid_peewee_conn/archive/master.zip

Setup
=======

Once ``pyramid_peewee_conn`` is installed, you must use the ``config.include``
mechanism to include it into your Pyramid project's configuration.  In your
Pyramid project's ``__init__.py``:

.. code-block:: python

   config = Configurator(.....)
   config.include('pyramid_peewee_conn')

Alternately you can use the ``pyramid.includes`` configuration value in your
``.ini`` file:

.. code-block:: ini

   [app:myapp]
   pyramid.includes = pyramid_peewee_conn

Using
=======

For ``pyramid_peewee_conn`` to work properly, you must add at least one
setting to your of your Pyramid's ``.ini`` file configuration (or to the
``settings`` dictionary if you're not using ini configuration):
``peewee.urls``.  For example:

.. code-block:: ini

   [app:myapp]
   # ...
   peewee.url = postgres://username:password@hostname:port/database_name
   # ...

The ``peewee.url`` parameter is a URL defined in the peewee documentation
`Connecting using a Database URL <https://peewee.readthedocs.org/en/latest/peewee/database.html#connecting-using-a-database-url>`_ 

Once you've both included the ``pyramid_peewee_conn`` into your configuration
via ``config.include('pyramid_peewee_conn')`` and you've added a
``peewee.url`` setting to your configuration, you can then use the
``pyramid_peewee_conn.get_db()`` API in your Pyramid application, most
commonly in a model defintion:

.. code-block:: python

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

The ``pyramid_peewee_conn.get_db()`` API returns a peewee.Database instance which 
you've specified via ``peewee.url`` in your configuration.


Attention
==========

Since the peewee database url is configure in ini file, the API ``pyramid_peewee_conn.get_db()`` 
must use after the instance of ``pyramid.config.Configurator`` has been created and this package 
has been included. In other words, if you configure this package via ini file like this:

.. code-block:: ini

    [app:myapp]
    # ...
    pyramid.includes = pyramid_peewee_conn
    # ...

You can use ``pyramid_peewee_conn.get_db()`` after the instance of ``pyramid.config.Configurator``
has been created. if you configure this package imperatively, you must use ``pyramid_peewee_conn.get_db()``
after the ``pyramid.config.Configurator.include()`` method has called by pass `'pyramid_peewee_conn'`.

.. code-block:: python

    from pyramid.config import Configurator

    def main(global_config, **settings):
        config = Configurator(settings=settings)
        # Now you can use get_db() if you configure this package in ini file.
        config.include('pyramid_peewee_conn')
        # Or you can use get_db() at this time.


Delay Initializtion
====================

There are some cases that need use the database before the ``pyramid.config.Configurator`` has
been instantiated. For example, a Model class is the configurator's root_factory, or by any
reason of, you need import the models in the `__init__.py` file.

In these cases, you can use ``pyramid_peewee_conn.get_proxy()`` instead of
``pyramid_peewee_conn.get_db()``, the parameters of ``get_proxy()`` is as same as ``get_db()``.

The ``pyramid_peewee_conn.get_proxy()`` returns an ``peewee.Proxy`` instance which will initialize
automatically at that time when ``pyramid.config.Configurator`` include this package.

Now, you can use peewee database before the ``pyramid.config.Configurator`` has been instantiated.
But you can't do any database opration before ``pyramid.config.Configurator`` has been instantiated.

.. note::
    
    The proxy which ``pyramid_peewee_conn.get_proxy()`` will never initialize except this package
    was included next time or call ``pyramid_peewee_conn.init_proxies()`` explicit. You can get more
    information in the API's docstring.

Named Databases
===============

If you need to use more than one database in your Pyramid application,
you can use *named* databases via configuration.  Named databases are
specified by ``peewee.url.thename`` in settings configuration.  For
example:

.. code-block:: ini

   [app:myapp]
   # ...
   peewee.url = postgres://username:password@hostname:port/database_name
   peewee.url.memory = sqlite:///:memory:
   # ...

Once this is done, you can use ``pyramid_peewee_conn.get_db()`` to
obtain a reference to each of the named databases:

.. code-block:: python

    db = get_db() # main database
    memory_db = get_db('memory')

The ``peewee.url.memory`` parameter example above is a URL which
describes peewee database, in the same format as ``peewee.url``.  You can
combine named and unnamed database configuration in the same application.
You can also use named databases without a main database.

Another config format
======================

Perhaps you had used pyramid_peewee, which config ``peewee.urls`` in the ini configure file like this:

.. code-block:: ini

    [app:myapp]
    # ...
    peewee.urls = postgres://username:password@hostname:port/database_1
        sqlite:///test.db
    # ...

This config format is supported. In this case, the database name is the database name.
The prior configuration is equal to the next:

.. code-block:: ini

    [app:myapp]
    # ...
    peewee.url = postgres://username:password@hostname:port/database_1
    peewee.url.database_1 = postgres://username:password@hostname:port/database_1
    peewee.url.test.db = sqlite:///test.db
    # ...

APIs
=======

This package offer three API:

- pyramid_peewee_conn.get_db()
- pyramid_peewee_conn.get_proxy()
- pyramid_peewee_conn.init_proxies()

The usage of these function you can found in there own's docstring via builtin ``help(obj)``.

If you found there were more functions or classes else in the souce code, it maybe changed in future.

Conflict
==========

Once there are both two format configure and have some database conflict, 
the explicit configuration will be used.

.. code-block:: ini

    [app:myapp]
    # ...
    peewee.url = postgres://user:pass@host:port/database
    peewee.url.db1 = mysql://user:pass@host:port/database
    peewee.urls = 
        mysql://user:pass@host:port/db1
        postgres://user:pass@host:port/database
    # ...

The prior configuration is equal next:

.. code-block:: ini

    [app:myapp]
    # ...
    peewee.url = postgres://user:pass@host:port/database
    peewee.url.db1 = mysql://user:pass@host:port/database
    peewee.url.database = postgres://user:pass@host:port/database
    # ...