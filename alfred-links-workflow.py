#!/usr/bin/python
# encoding: utf-8

import logging
from logging.config import fileConfig
import sys

fileConfig('logging_config.ini')

from links.handlers.route import route
from links.util import workflow

log = logging.getLogger('links')


def main(wf):
    route(wf.args)
    log.info('Workflow response complete')

if __name__ == '__main__':
    log.info('begin alfred-links-workflow')
    wf = workflow()
    sys.exit(wf.run(main, text_errors='--commit' in wf.args))
