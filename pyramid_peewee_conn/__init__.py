import sys
import logging

from playhouse import db_url


_log = logging.getLogger(__name__)
_data = {
    'urls': {},
    'databases': {},
    'proxies': {}
}


def includeme(config):
    urls = _data['urls']
    prefix = 'peewee.url.'
    settings = config.registry.settings
    # Compatible with the pyramid_peewee
    old_version_urls = settings.get('peewee.urls', '').split()
    for url in old_version_urls:
        db_info = db_url.parse(url)
        db_name = db_info['database']
        urls[db_name] = url
    old_main_url = old_version_urls[0] if old_version_urls else ''

    main_url = settings.get('peewee.url', '') or old_main_url
    if main_url:
        urls[None] = main_url

    for k, url in settings.items():
        if k.lower().startswith(prefix):
            db_name = k[len(prefix):]
            urls[db_name] = url

    init_proxies()


def get_db(name=None):
    '''get_db(name) -> instance of peewee.Database

    Return an object is an instance of ``peewee.Database``.
    Parameter name is an database name which defined in config file.
    If name is None or didn't offer, return the default database.

    This function can't be use before ``pyramid_peewee_conn`` has be
    included. In that case, you can use get_proxy().
    '''
    urls = _data['urls']
    databases = _data['databases']
    try:
        url = urls[name]
    except KeyError:
        _log.error('Database %s has not configured!', name)
        sys.exit(1)
    return databases.setdefault(name, db_url.connect(url))


def get_proxy(name=None):
    '''get_proxy(name) -> instance of peewee.Proxy

    Return an object is an instance of ``peewee.Proxy``.
    The parameter name is as same as get_db. The returned proxy
    will initialized until next ``init_proxies()`` was called.

    When pyramid application including ``pyramid_peewee_conn``,
    the function ``init_proxies()`` will be called automatically.
    '''
    proxies = _data['proxies']
    return proxies.setdefault(name, db_url.Proxy())


def init_proxies():
    '''Initialize the proxies which ``get_proxy()`` returned.abs

    Note before pyramid application has included ``pyramid_peewee_conn``,
    this method can't be called or it will log some error message and
    exit the application. If your logging's setting don't print any error
    message on screen, you can't found any prompt message.
    '''
    proxies = _data['proxies']
    for db_name, proxy in proxies.items():
        database = get_db(db_name)
        if proxy.obj is None:
            proxy.initialize(database)
