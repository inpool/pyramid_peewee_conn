from pyramid.config import Configurator
from peewee import SqliteDatabase, PostgresqlDatabase, MySQLDatabase

from pyramid_peewee_conn import get_db


def load_config(style='new'):
    settings = {'new': {'peewee.url': 'sqlite:///:memory:',
                        'peewee.url.test': 'postgres://user:password@hostname/pgdbname', },
                'old': {'peewee.urls': (
                    'sqlite:///test.db',
                    'mysql://user:password@hostname/mysqldb',
                    'mysql://user:password@hostname/test'
                )},
                'combined': {}, }
    settings['combined'].update(settings['new'])
    settings['combined'].update(settings['old'])

    config = Configurator(settings=settings[style])
    config.include('pyramid_peewee_conn')


def test_get_db_combined_style():
    '''
    peewee.url = sqlite:///:memory:
    peewee.url.test = postgres://user:password@hostname/pgdbname
    peewee.urls =
        sqlite:///test.db
        mysql://user:password@hostname/mysqldb
        mysql://user:password@hostname/test
    '''
    load_config('combined')
    db_default = get_db()
    db_test = get_db('test')
    db_test_db = get_db('test.db')
    db_mysqldb = get_db('mysqldb')

    assert isinstance(db_default, SqliteDatabase)
    assert db_default.database == ':memory:'

    assert isinstance(db_test, PostgresqlDatabase)
    assert db_test.database == 'pgdbname'

    assert isinstance(db_test_db, SqliteDatabase)
    assert db_test_db.database == 'test.db'

    assert isinstance(db_mysqldb, MySQLDatabase)
    assert db_mysqldb.database == 'mysqldb'


def test_get_db_new_style():
    '''
    peewee.url = sqlite:///:memory:
    peewee.url.test = postgres://user:password@hostname/pgdbname
    '''
    load_config('new')
    db_default = get_db()
    db_test = get_db('test')

    assert isinstance(db_default, SqliteDatabase)
    assert db_default.database == ':memory:'

    assert isinstance(db_test, PostgresqlDatabase)
    assert db_test.database == 'pgdbname'


def test_get_db_old_style():
    '''
    peewee.urls =
        sqlite:///test.db
        mysql://user:password@hostname/mysqldb
        mysql://user:password@hostname/test
    '''

    load_config('old')
    db_default = get_db()
    db_test_db = get_db('test.db')
    db_mysqldb = get_db('mysqldb')
    db_test = get_db('test')

    assert isinstance(db_default, SqliteDatabase)
    assert isinstance(db_test_db, SqliteDatabase)
    assert db_default.database == db_test_db.database == 'test.db'

    assert isinstance(db_mysqldb, MySQLDatabase)
    assert db_mysqldb.database == 'mysqldb'

    assert isinstance(db_test, MySQLDatabase)
    assert db_test.database == 'test'
