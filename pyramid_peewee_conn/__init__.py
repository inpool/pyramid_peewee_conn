import sys
import logging

from playhouse import db_url


_log = logging.getLogger(__name__)
__urls = {}
__proxies = {}


def includeme(config):
    prefix = 'peewee.url.'
    settings = config.registry.settings
    # Compatible with the pyramid_peewee
    old_version_urls = settings.get('peewee.urls', [])
    main_url = settings.get('peewee.url', None)
    if main_url:
        __urls[None] = main_url
    for url in old_version_urls:
        db_info = db_url.parse(url)
        db_name = db_info['database']
        __urls[db_name] = url
    for k, v in settings.items():
        if k.lower().startswith(prefix):
            db_name = k[len(prefix):]
            __urls[db_name] = v


def get_db(name=None):
    try:
        url = __urls[name]
    except KeyError:
        _log.error('Database %s has not configured!' % name)
        sys.exit(1)
    return __proxies.setdefault(name, db_url.connect(url))
