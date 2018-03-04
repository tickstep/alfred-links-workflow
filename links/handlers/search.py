# encoding: utf-8

from datetime import datetime
from links import icons, config
from links.models.preferences import Preferences
from links.util import workflow
from links.api import search_api
import logging
from logging.config import fileConfig
fileConfig('logging_config.ini')
log = logging.getLogger('links')


def filter(args):
    prefs = Preferences.current_prefs()

    log.info(args)
    queryWord = ''
    if len(args) >= 2:
        queryWord = ''
        for idx in range(1, len(args)):
            w = args[idx]
            queryWord = "%s %s" % (queryWord, w)
    queryWord = queryWord.strip()

    if not workflow().stored_data(config.KC_ENABLE_SEARCH):
        log.info('enable search false')
        log.info('store last time keyword: %s' % workflow().stored_data(config.KC_LAST_TIME_QUERY_WORD))
        # the same keyword means this is page navigate action
        if queryWord != workflow().stored_data(config.KC_LAST_TIME_QUERY_WORD):
            workflow().add_item(
                u'需要先返回主菜单才能进行新的搜索',
                autocomplete=' ', icon=icons.BACK
            )
            workflow().store_data(config.KC_ENABLE_SEARCH, False)
            return

    workflow().add_item(
        u'返回主菜单',
        autocomplete=' ', icon=icons.BACK
    )
    log.info('begin to search')
    workflow().store_data(config.KC_ENABLE_SEARCH, False)

    # page index
    scmd = args[0]
    idx = scmd.find(':')
    if idx > 0:
        pidx = int(scmd[idx + 1:])
        workflow().store_data(config.KC_CURRENT_PAGE_INDEX, pidx)
    else:
        workflow().store_data(config.KC_CURRENT_PAGE_INDEX, 0)

    # search
    log.info('begin to search %s' % (queryWord))
    workflow().store_data(config.KC_LAST_TIME_QUERY_WORD, queryWord)
    result = search_api.search(queryWord, workflow().stored_data(config.KC_CURRENT_PAGE_INDEX) * prefs.maxResultCount, prefs.maxResultCount)

    if result['statusCode'] == 0:
        if 'data' in result and result['data'] != None and len(result['data']) > 0:

            # update query count statistic
            queryCount = result['data']['queryCount']
            if 'max' in queryCount:
                workflow().store_data(config.KC_MAX_COUNT, queryCount['max'])
            if 'reserved' in queryCount:
                workflow().store_data(config.KC_RESERVED_COUNT, queryCount['reserved'])

            # vip
            if 'vip' in queryCount:
                log.info('vip = %s' % (queryCount['vip']))
                workflow().store_data(config.KC_VIP_STATUS, queryCount['vip'])

            # download link item
            items = result['data']['items']
            if items == None or len(items) == 0:
                workflow().add_item(u'没有查询到结果，更改关键词再试试吧')

            else:
                if len(items) > 1:
                    cp = ""
                    for item in items:
                        cp = cp + item['name'] + '\n'
                        cp = cp + pickDlLinks(item) + "\n"

                    workflow().add_item(u'⌘+C 复制查询到的全部下载链接', copytext=cp, largetext=cp,
                                        icon=icons.COPY)

                for item in items:
                    createDate = datetime.utcfromtimestamp(int(item['createDate'] / 1000))
                    ts = u'更新时间：{0}年{1}月{2}日'.format(createDate.year, createDate.month, createDate.day)
                    dl = pickDlLinks(item)
                    workflow().add_item(item['name'], ts, copytext=dl,
                                        largetext=item['name'] + '\n' + dl,
                                        icon=icons.APP)

                # next page has?
                if len(items) >= prefs.maxResultCount:
                    workflow().add_item(
                        u'下一页',
                        autocomplete='-search:%s %s' % (workflow().stored_data(config.KC_CURRENT_PAGE_INDEX) + 1, queryWord), icon=icons.NEXT
                    )

        else:
            workflow().add_item(u'没有查询到结果，更改关键词再试试吧')
    else:
        workflow().add_item(result['message'])


def commit(args, modifier=None):
    log.info('search commit')
    queryWord = ''
    if len(args) >= 2:
        queryWord = ''
        for idx in range(1, len(args)):
            w = args[idx]
            queryWord = "%s %s" % (queryWord, w)
    queryWord = queryWord.strip()
    print '-search-url %s' % (queryWord)


def pickDlLinks(item):
    dlStr = u'你没有权限访问下载链接\n'
    if 'dlUrl' in item:
        if 'url' in item['dlUrl'] and len(item['dlUrl']['url']) > 0:
            dlStr = item['dlUrl']['url'] + "\n"
        elif 'torrentUrl' in item['dlUrl'] and len(item['dlUrl']['torrentUrl']) > 0:
            dlStr = item['dlUrl']['torrentUrl'] + "\n"
        elif 'baiduDiskUrl' in item['dlUrl'] and len(item['dlUrl']['baiduDiskUrl']) > 0:
            dlStr = item['dlUrl']['baiduDiskUrl'] + "\n"

    if 'password' in item and len(item['password']) > 0:
        dlStr = dlStr + u"解压密码： " + item['password'] + "\n"
    return dlStr

