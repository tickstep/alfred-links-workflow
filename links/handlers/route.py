# encoding: utf-8

import os
import re

from links import auth, config
from links.util import workflow

import logging
from logging.config import fileConfig

from workflow import PasswordNotFound

fileConfig('logging_config.ini')
log = logging.getLogger('links')

COMMAND_PATTERN = re.compile(r'^[^\w\s]+', re.UNICODE)
ACTION_PATTERN = re.compile(r'^\W+', re.UNICODE)


def route(args):
    log.info(u'in route process')

    # debug
    # try:
    #     workflow().delete_password(config.KC_OAUTH_TOKEN)
    # except PasswordNotFound as e:
    #     log.error(e)

    handler = None
    command = []
    command_string = ''
    action = 'none'

    if args:
        command_string = args[0]
        # log.info('route args')
        # for arg in args:
        #     log.info(arg)
    else:
        log.info('route with empty args')

    command_string = re.sub(COMMAND_PATTERN, '', command_string)
    command = re.split(r' +', command_string)

    if command:
        action = re.sub(ACTION_PATTERN, '', command[0]) or 'none'

    if 'about'.find(action) == 0:
        from links.handlers import about
        handler = about
    elif not auth.is_authorized():
        from links.handlers import login
        handler = login
    elif 'logout'.find(action) == 0:
        from links.handlers import logout
        handler = logout
    elif 'moreQuery'.find(action) == 0:
        from links.handlers import query_count
        handler = query_count
    elif 'pref'.find(action) == 0:
        from links.handlers import preferences
        handler = preferences

    elif 'search'.find(action) == 0:
        from links.handlers import search
        handler = search

    # If the command starts with a space (no special keywords), the workflow
    # creates a new task
    elif not command_string:
        from links.handlers import welcome
        handler = welcome

    else:
        from links.handlers import welcome
        handler = welcome

    if handler:
        if '--commit' in args:
            modifier = re.search(r'--(alt|cmd|ctrl|fn)\b', ' '.join(args))

            if modifier:
                modifier = modifier.group(1)

            handler.commit(command, modifier)
        else:
            handler.filter(command)
            workflow().send_feedback()

