# encoding: utf-8

from links import auth, icons, util


def filter(args):
    util.workflow().add_item(
        u'确定退出登录？',
        u'退出后您需要再次登录链刻账户才能正常使用workflow',
        arg=' '.join(args),
        valid=True,
        icon=icons.CHECKMARK
    )

    util.workflow().add_item(
        u'取消',
        autocomplete=' ',
        icon=icons.CANCEL
    )


def commit(args, modifier=None):
    auth.deauthorize()
    util.workflow().clear_data()
    util.workflow().clear_cache()

    # print '您已经成功退出登录'
    # print 'Logout success'
    print '已退出登录'
