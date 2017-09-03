# encoding: utf-8

import re

from links import auth, icons, config
from links.util import relaunch_alfred, workflow

import logging
from logging.config import fileConfig
fileConfig('logging_config.ini')
log = logging.getLogger('links')

ACTION_PATTERN = re.compile(r'^\W+', re.UNICODE)


def filter(args):

    workflow().add_item(
        u'请先登录',
        u'使用您在链刻网注册的账号进行登录',
        arg=' '.join('login'),
        valid=True, icon=icons.ACCOUNT
    )

    workflow().add_item(
        u'注册账号',
        u'没有账号？前往我们的官方网站进行免费注册',
        arg=' '.join('register'),
        valid=True, icon=icons.HASHTAG
    )

    workflow().add_item(
        u'关于我们',
        u'查看我们的相关信息',
        autocomplete='-about ',
        icon=icons.INFO
    )


def commit(args, modifier=None):
    if args:
        action = args[0]

        if 'login'.find(action) == 0:
            # login
            log.info('begin to login')
            auth.authorize()
            return

        elif 'register'.find(action) == 0:
            # register
            log.info('begin to register')
            import webbrowser
            webbrowser.open(config.LK_REGISTER_URL)
            return

    print '没有找到对应的操作'
