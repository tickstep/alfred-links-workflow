from datetime import time, timedelta

from links.util import workflow
import logging
from logging.config import fileConfig
fileConfig('logging_config.ini')
log = logging.getLogger('links')

KEY_MAX_RESTUL_COUNT = 'links_max_result_count'
KEY_THEME = 'links_theme'

THEME_DARK = 'dark'
THEME_LIGHT = 'light'


class Preferences(object):

    _current_prefs = None

    @classmethod
    def current_prefs(cls):
        if not cls._current_prefs:
            cls._current_prefs = Preferences(workflow().stored_data('links_prefs'))
        if not cls._current_prefs:
            cls._current_prefs = Preferences({})
        log.info(cls._current_prefs)
        return cls._current_prefs

    def __init__(self, data):
        self._data = data or {}

    def _set(self, key, value):
        if self._data.get(key) != value:
            self._data[key] = value
            workflow().store_data('links_prefs', self._data)

    def _get(self, key, default=None, type=str):
        value = self._data.get(key)

        if value is None and default is not None:
            value = default

        return value

    @property
    def maxResultCount(self):
        return self._get(KEY_MAX_RESTUL_COUNT) or 7

    @maxResultCount.setter
    def maxResultCount(self, count):
        self._set(KEY_MAX_RESTUL_COUNT, count)

    @property
    def theme(self):
        return self._get(KEY_THEME, None)

    @theme.setter
    def theme(self, theme):
        self._set(KEY_THEME, theme)

