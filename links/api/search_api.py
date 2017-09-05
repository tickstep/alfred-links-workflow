# encoding: utf-8

import sys
from datetime import datetime
import requests
import json
import time
import os
from links import icons, config
from links.util import workflow
from links.models.preferences import Preferences
import logging
from logging.config import fileConfig
fileConfig('logging_config.ini')
log = logging.getLogger('links')


def getAlfredVersion(wf):
    # alfred workflow version
    v = wf.alfred_version.tuple
    return "{0}.{1}.{2}".format(v[0], v[1], v[2])


def getWorkflowVersion():
    with open('version', 'r') as file:
        ver = file.readlines()[0]
    return ver.strip()


def search(query, offset, size):
    localResult = {
        'statusCode': 0,
        'message': '',
        'data': []
    }

    appKey = workflow().get_password(config.KC_OAUTH_TOKEN)
    log.info('appKey: %s' % (appKey))

    # query the keyword from web server
    prefs = Preferences.current_prefs()
    session = requests.session()
    formData = {
        'keyword': query,
        'from': offset,
        'size': size
    }
    resp = session.post(
        url=config.LK_SEARCH_APP_URL,
        headers={
            'User-Agent': 'alfred/{0} workflow/{1}'.format(getAlfredVersion(workflow()), getWorkflowVersion()),
            'Authorization': appKey,
            'Content-Type': 'application/json; charset=UTF-8'
        },
        data=json.dumps(formData),
        timeout=60)
    if resp.status_code == 200:
        log.info('search respond success')
        result = json.loads(resp.text)
        return result
    else:
        log.info('search respond failed')
        localResult['message'] = u'网络错误，请稍后重试'
        return localResult
