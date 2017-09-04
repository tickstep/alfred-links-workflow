# encoding: utf-8

from links import auth, icons, config
from links.util import relaunch_alfred, workflow
from links.models.preferences import Preferences

import logging
from logging.config import fileConfig
fileConfig('logging_config.ini')
log = logging.getLogger('links')


def filter(args):

    workflow().add_item(
        u'查询结果个数',
        u'设置服务器返回结果的最大个数',
        arg='-pref resultCount', valid=True, icon=icons.LIST
    )

    workflow().add_item(
        u'切换主题',
        u'在白色和黑色图标直接切换',
        arg='-pref retheme',
        valid=True,
        icon=icons.PAINTBRUSH
    )

    workflow().add_item(
        u'返回主菜单',
        autocomplete=' ', icon=icons.BACK
    )


def commit(args, modifier=None):
    prefs = Preferences.current_prefs()
    relaunch_command = 'lk '

    if 'resultCount' in args:
        pass

    elif 'retheme' in args:
        prefs.theme = 'light' if icons.icon_theme() == 'dark' else 'dark'

    if relaunch_command:
        relaunch_alfred(relaunch_command)
