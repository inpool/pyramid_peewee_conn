import sys
import logging

from playhouse import db_url


_log = logging.getLogger(__name__)
_urls = {}
_dbs = {}


def includeme(config):
    _urls.clear()
    _dbs.clear()
    prefix = 'peewee.url.'
    settings = config.registry.settings
    # Compatible with the pyramid_peewee
    old_version_urls = settings.get('peewee.urls', [])
    for url in old_version_urls:
        db_info = db_url.parse(url)
        db_name = db_info['database']
        _urls[db_name] = url
    old_main_url = old_version_urls[0] if old_version_urls else ''

    main_url = settings.get('peewee.url', '') or old_main_url
    if main_url:
        _urls[None] = main_url

    for k, url in settings.items():
        if k.lower().startswith(prefix):
            db_name = k[len(prefix):]
            _urls[db_name] = url


def get_db(name=None):
    try:
        url = _urls[name]
    except KeyError:
        _log.error('Database %s has not configured!', name)
        sys.exit(1)
    return _dbs.setdefault(name, db_url.connect(url))
