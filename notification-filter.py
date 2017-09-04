# encoding: utf-8

import logging
from logging.config import fileConfig
import sys

reload(sys)
sys.setdefaultencoding('utf8')

fileConfig('logging_config.ini')
from links.util import workflow

log = logging.getLogger('links')


def main(wf):
    if len(wf.args) == 0:
        return
    outputString = wf.args[0]
    # log.info(outputString)
    if len(outputString) == 0:
        return
    if outputString.find('<?xml') == 0:  # filter exception output
        return
    if outputString.find('-search-url') != 0:
        print outputString


if __name__ == '__main__':
    log.info('begin notification filter')
    wf = workflow()
    sys.exit(wf.run(main, text_errors='--commit' in wf.args))