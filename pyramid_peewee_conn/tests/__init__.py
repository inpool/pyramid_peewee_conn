'''
The unit test for pyramid_peewee_conn using pytest.

Author: Inpool
Email: inpool@126.com
'''

from os.path import abspath, dirname, join as pathjoin
from configparser import ConfigParser, ExtendedInterpolation

from pyramid.config import Configurator
from peewee import SqliteDatabase, PostgresqlDatabase, MySQLDatabase, Proxy
from pytest import raises

from pyramid_peewee_conn import _data, get_db, get_proxy, init_proxies

CFG_FILE = abspath(pathjoin(dirname(__file__), 'config.ini'))
CONFIG = ConfigParser(interpolation=ExtendedInterpolation())
CONFIG.read(CFG_FILE)


def setup_function():
    'Run before each testing'
    for data in _data.values():
        data.clear()


def load_config(style):
    'Instantiate Configurator with specified setting'

    config = Configurator(settings=CONFIG[style])
    config.include('pyramid_peewee_conn')


def test_get_db_before_included():
    "Test get_db() when Configurator hasn't been instantiated"

    with raises(SystemExit):
        get_db()


def test_get_db_combined_style():
    'Test get_db() when config as both new style and old style present'

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
    'Test get_db() when config as new style'

    load_config('new')
    db_default = get_db()
    db_test = get_db('test')

    assert isinstance(db_default, SqliteDatabase)
    assert db_default.database == ':memory:'

    assert isinstance(db_test, PostgresqlDatabase)
    assert db_test.database == 'pgdbname'


def test_get_db_old_style():
    'Test get_db() when config as old style'

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


def test_get_proxy():
    "Test get_proxy()"

    proxy = get_proxy()

    assert isinstance(proxy, Proxy)
    assert proxy is _data['proxies'][None]
    assert proxy.obj is None

    load_config('new')

    assert proxy.obj is get_db()


def test_init_proxies_before_included():
    "Test init_proxies() when Configurator hasn't been instantiated"

    proxy = get_proxy()
    with raises(SystemExit):
        init_proxies()

    assert proxy.obj is None


def test_init_proxies():
    "Test get_db() when Configurator hasbeen instantiated"

    load_config('new')
    proxy = get_proxy()
    init_proxies()

    assert proxy.obj is get_db()

    proxy_undefined = get_proxy('undefined')
    with raises(SystemExit):
        init_proxies()
