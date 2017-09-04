# encoding: utf-8

from datetime import datetime
from links import icons, config
from links.util import workflow
from links.api import search_api
import logging
from logging.config import fileConfig
fileConfig('logging_config.ini')
log = logging.getLogger('links')


def filter(args):

    if not workflow().stored_data(config.KC_ENABLE_SEARCH):
        workflow().add_item(
            u'先返回主菜单再进行搜索',
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

    # search
    queryWord = ''
    if len(args) >= 2:
        queryWord = ''
        for idx in range(1, len(args)):
            w = args[idx]
            queryWord = "%s %s" % (queryWord, w)
    queryWord = queryWord.strip()
    log.info('begin to search %s' % (queryWord))
    result = search_api.search(queryWord)

    if result['statusCode'] == 0:
        if 'data' in result and result['data'] != None and len(result['data']) > 0:

            # update query count statistic
            queryCount = result['data']['queryCount']
            if 'max' in queryCount:
                workflow().store_data(config.KC_MAX_COUNT, queryCount['max'])
            if 'reserved' in queryCount:
                workflow().store_data(config.KC_RESERVED_COUNT, queryCount['reserved'])

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
                    ts = u'{0}年{1}月'.format(createDate.year, createDate.month)
                    dl = pickDlLinks(item)
                    workflow().add_item(item['name'], ts + ' / ' + item['dlUrl']['url'], copytext=dl,
                                        largetext=item['name'] + '\n' + dl,
                                        icon=icons.APP)
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
    str = ""
    if len(item['dlUrl']['url']) > 0:
        str = item['dlUrl']['url'] + "\n"
    if len(item['dlUrl']['baiduDiskUrl']) > 0:
        str = str + item['dlUrl']['url'] + "\n"
    return str

