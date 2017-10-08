from pyramid.config import Configurator
from peewee import SqliteDatabase, PostgresqlDatabase, MySQLDatabase

from pyramid_peewee_conn import get_db


def setup_module(_):
    settings = {
        'peewee.url': 'sqlite:///:memory:',
        'peewee.url.test': 'postgres://user:password@hostname/pgdbname',
        'peewee.urls': (
            'sqlite:///test.db',
            'mysql://user:password@hostname/mysqldb',
            'mysql://user:password@hostname/test'
        )}
    config = Configurator(settings=settings)
    config.include('pyramid_peewee_conn')


def test_get_db():
    db_main = get_db()
    db_test = get_db('test')
    db_test_db = get_db('test.db')
    db_mysqldb = get_db('mysqldb')

    assert isinstance(db_main, SqliteDatabase)
    assert db_main.database == ':memory:'

    assert isinstance(db_test, PostgresqlDatabase)
    assert db_test.database == 'pgdbname'

    assert isinstance(db_test_db, SqliteDatabase)
    assert db_test_db.database == 'test.db'

    assert isinstance(db_mysqldb, MySQLDatabase)
    assert db_mysqldb.database == 'mysqldb'
