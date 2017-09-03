# encoding: utf-8

from links import auth, icons, util, config


def filter(args):
    util.workflow().add_item(
        u'需要更多查询次数？',
        u'立即前往我们的官方网站获取',
        arg=' '.join(args),
        valid=True,
        icon=icons.OPEN
    )

    util.workflow().add_item(
        u'取消',
        autocomplete=' ',
        icon=icons.CANCEL
    )


def commit(args, modifier=None):
    import webbrowser
    webbrowser.open(config.LK_GET_MORE_QUERY_COUNT_URL)

