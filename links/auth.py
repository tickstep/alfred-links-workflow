# encoding: utf-8

from workflow import PasswordNotFound

from links import config
from links.util import relaunch_alfred, workflow
import logging
from logging.config import fileConfig
fileConfig('logging_config.ini')
log = logging.getLogger('links')


def authorize():
    from multiprocessing import Process
    import urllib
    import webbrowser

    workflow().store_data('auth', 'started')

    state = new_oauth_state()
    data = urllib.urlencode({
        'client_id': config.LK_CLIENT_ID,
        'redirect_uri': 'http://localhost:6311',
        'state': state
    })
    url = '%s?%s' % (config.LK_OAUTH_URL, data)

    # Start a server to await the redirect URL request after authorizing
    server = Process(target=await_token)
    server.start()

    # Open the authorization prompt in the default web browser
    webbrowser.open(url)


def deauthorize():
    try:
        workflow().delete_password(config.KC_OAUTH_TOKEN)
    except PasswordNotFound:
        pass


def is_authorized():
    return oauth_token() is not None


def handle_authorization_url(url):
    import urlparse

    # Parse query data & params to find out what was passed
    parsed_url = urlparse.urlparse(url)
    params = urlparse.parse_qs(parsed_url.query)

    # request is either for a file to be served up or our test
    if 'appKey' in params and validate_oauth_state(params['state'][0]):
        workflow().save_password(config.KC_OAUTH_TOKEN, params['appKey'][0])
        workflow().delete_password(config.KC_OAUTH_STATE)

        if 'maxCount' in params:
            workflow().store_data(config.KC_MAX_COUNT, params['maxCount'][0])
        if 'reservedCount' in params:
            workflow().store_data(config.KC_RESERVED_COUNT, params['reservedCount'][0])
        if 'userName' in params:
            workflow().store_data(config.KC_USER_NAME, params['userName'][0])
        if 'vip' in params:
            workflow().store_data(config.KC_VIP_STATUS, params['vip'][0])

        print '您已经成功登录'
        return True
    else:
        workflow().store_data('auth', 'login error')
        print '登录失败，请稍后重试'

    # Not a valid URL
    return False


def oauth_token():
    try:
        return workflow().get_password(config.KC_OAUTH_TOKEN)
    except PasswordNotFound:
        return None


def client_id():
    return config.LK_CLIENT_ID


def oauth_state():
    try:
        return workflow().get_password(config.KC_OAUTH_STATE)
    except PasswordNotFound:
        return None


def new_oauth_state():
    import random
    import string

    state_length = 20
    state = ''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(state_length))

    workflow().save_password(config.KC_OAUTH_STATE, state)

    return state


def validate_oauth_state(state):
    return state == oauth_state()


def await_token():
    import SimpleHTTPServer
    import SocketServer

    class OAuthTokenResponseHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

        def do_GET(self):
            log.info('redirect from server: ' + self.path)
            auth_status = handle_authorization_url(self.path)

            if not auth_status:
                self.path = 'www/' + self.path
            elif auth_status is True:
                self.path = 'www/authorize.html'
            else:
                self.path = 'www/decline.html'

            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
            relaunch_alfred()

    server = SocketServer.TCPServer(
        ("", config.LK_OAUTH_PORT), OAuthTokenResponseHandler)

    server.timeout = config.LK_OAUTH_TIMEOUT
    server.handle_request()
