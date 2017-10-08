from os.path import abspath, dirname, join as pathjoin
from configparser import ConfigParser, ExtendedInterpolation

from pyramid.config import Configurator
from peewee import SqliteDatabase, PostgresqlDatabase, MySQLDatabase
from pytest import raises

from pyramid_peewee_conn import get_db, _data

CFG_FILE = abspath(pathjoin(dirname(dirname(__file__)), 'pytest.ini'))
CONFIG = ConfigParser(interpolation=ExtendedInterpolation())
CONFIG.read(CFG_FILE)


def setup_function():
    for data in _data.values():
        data.clear()


def load_config(style):
    style_name = 'case_' + style
    config = Configurator(settings=CONFIG[style_name])
    config.include('pyramid_peewee_conn')


def test_get_db_before_included():
    with raises(SystemExit):
        get_db()


def test_get_db_combined_style():
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
