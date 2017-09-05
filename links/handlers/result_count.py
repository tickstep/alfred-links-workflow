# encoding: utf-8

from links import icons, config
from links.util import workflow, relaunch_alfred
from links.models.preferences import Preferences


def filter(args):
    prefs = Preferences.current_prefs()

    icon = icons.TASK
    if prefs.maxResultCount == 7:
        icon = icons.TASK_COMPLETED
    workflow().add_item(
        u'设定最大值为 7',
        arg='-result_count max_7', valid=True, icon=icon
    )

    icon = icons.TASK
    if prefs.maxResultCount == 20:
        icon = icons.TASK_COMPLETED
    workflow().add_item(
        u'设定最大值为 20',
        u'VIP账户才能生效',
        arg='-result_count max_20', valid=True, icon=icon
    )

    workflow().add_item(
        u'返回主菜单',
        autocomplete=' ', icon=icons.BACK
    )


def commit(args, modifier=None):
    prefs = Preferences.current_prefs()
    relaunch_command = 'lk '

    if 'max_7' in args:
        prefs.maxResultCount = 7

    elif 'max_20' in args:
        prefs.maxResultCount = 20

    if relaunch_command:
        relaunch_alfred(relaunch_command)
