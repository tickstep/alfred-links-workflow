# encoding: utf-8
import webbrowser

from datetime import datetime
from links import icons, config
from links.util import workflow
from links.api import search_api
import logging
from logging.config import fileConfig
fileConfig('logging_config.ini')
log = logging.getLogger('links')


def filter(args):
    log.info(args)

    if len(args) >= 2:
        queryWord = ''
        for w in args:
            queryWord = "%s %s" % (queryWord, w)

        queryWord = queryWord.strip()
        prompt = u'根据您输入的关键词搜索软件的下载链接'
        if len(queryWord) > 0:
            prompt = u'搜索软件下载链接：%s' % (queryWord)
            workflow().add_item(
                u'搜索',
                prompt,
                arg='-search %s' % (queryWord),
                autocomplete='-search %s' % (queryWord),
                icon=icons.SEARCH
            )
        else:
            workflow().add_item(
                u'搜索',
                u'根据您输入的关键词搜索软件的下载链接',
                autocomplete=' ',
                icon=icons.SEARCH
            )

    else:
        workflow().add_item(
            u'搜索',
            u'根据您输入的关键词搜索软件的下载链接',
            autocomplete=' ',
            icon=icons.SEARCH
        )
    workflow().store_data(config.KC_ENABLE_SEARCH, True)

    reservedCount = u'%s: %s 次,  %s: %s 次' % (u'本月剩余', workflow().stored_data(config.KC_RESERVED_COUNT), u'本月总共', workflow().stored_data(config.KC_MAX_COUNT))
    workflow().add_item(
        u'获取更多查询次数',
        reservedCount,
        autocomplete='-moreQuery',
        icon=icons.LINK
    )

    workflow().add_item(
        u'帮助文档',
        u'前往我们的官方网站查看相关帮助文档',
        arg='-document ',
        valid=True,
        icon=icons.LIST
    )

    logoutAccount = '%s: %s' % (u'退出您当前登录的账户', workflow().stored_data(config.KC_USER_NAME))
    workflow().add_item(
        u'退出登录',
        logoutAccount,
        autocomplete='-logout ',
        icon=icons.ACCOUNT
    )

    workflow().add_item(
        u'设置',
        autocomplete='-pref ',
        icon=icons.PREFERENCES
    )

    workflow().add_item(
        u'关于我们',
        u'查看我们的相关信息',
        autocomplete='-about ',
        icon=icons.INFO
    )


def commit(args, modifier=None):
    if 'document' in args:
        webbrowser.open(config.LK_ONLINE_DOC_URL)






