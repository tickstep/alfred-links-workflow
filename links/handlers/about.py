# encoding: utf-8

from links import icons, config
from links.util import workflow


def filter(args):
    workflow().add_item(
        u'访问官网',
        u'前往官方网站查看最新动态信息',
        arg='-about homepage', valid=True, icon=icons.INFO
    )

    workflow().add_item(
        u'您是开发者',
        u'前往我们Github主页',
        arg='-about github', valid=True, icon=icons.OPEN
    )

    workflow().add_item(
        u'更新版本',
        u'检测是否有新版本并进行更新',
        arg='-about update', valid=True, icon=icons.DOWNLOAD
    )

    workflow().add_item(
        u'返回主菜单',
        autocomplete=' ', icon=icons.BACK
    )


def commit(args, modifier=None):
    if 'update' in args:
        if workflow().start_update():
            print 'workflow已经请求进行更新中'
        else:
            print '您已经升级到最新版本了'
    elif 'homepage' in args:
        import webbrowser
        webbrowser.open(config.LK_HOMEPAGE_URL)
    elif 'github' in args:
        import webbrowser
        webbrowser.open(config.LK_GITHUB_HOMEPAGE_URL)

