from links.util import workflow
from links.models.preferences import Preferences
import logging
from logging.config import fileConfig
fileConfig('logging_config.ini')
log = logging.getLogger('links')

_icon_theme = None


def alfred_is_dark():
    # Formatted rgba(255,255,255,0.90)
    background_rgba = workflow().alfred_env['theme_background']
    if background_rgba:
        rgb = [int(x) for x in background_rgba[5:-6].split(',')]
        return (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255 < 0.5
    return False


def icon_theme():
    global _icon_theme
    if not _icon_theme:
        prefs = Preferences.current_prefs()
        log.info('theme = %s' % (prefs.theme))

        if prefs.theme:
            _icon_theme = prefs.theme
        else:
            _icon_theme = 'light' if alfred_is_dark() else 'dark'

    return _icon_theme

_icon_path = 'icons/%s/' % icon_theme()

ACCOUNT = _icon_path + 'account.png'
BACK = _icon_path + 'back.png'
CALENDAR = _icon_path + 'calendar.png'
CANCEL = _icon_path + 'cancel.png'
CHECKBOX = _icon_path + 'task.png'
CHECKBOX_SELECTED = _icon_path + 'task_completed.png'
CHECKMARK = _icon_path + 'checkmark.png'
DISCUSS = _icon_path + 'discuss.png'
DOWNLOAD = _icon_path + 'download.png'
HASHTAG = _icon_path + 'hashtag.png'
HELP = _icon_path + 'help.png'
HIDDEN = _icon_path + 'hidden.png'
INBOX = _icon_path + 'inbox.png'
INFO = _icon_path + 'info.png'
LINK = _icon_path + 'link.png'
LIST = _icon_path + 'list.png'
LIST_NEW = _icon_path + 'list_new.png'
NEXT_WEEK = _icon_path + 'next_week.png'
OPEN = _icon_path + 'open.png'
PAINTBRUSH = _icon_path + 'paintbrush.png'
PREFERENCES = _icon_path + 'preferences.png'
RADIO = _icon_path + 'radio.png'
RADIO_SELECTED = _icon_path + 'radio_selected.png'
RECURRENCE = _icon_path + 'recurrence.png'
REMINDER = _icon_path + 'reminder.png'
SEARCH = _icon_path + 'search.png'
SORT = _icon_path + 'sort.png'
STAR = _icon_path + 'star.png'
STAR_REMOVE = _icon_path + 'star_remove.png'
SYNC = _icon_path + 'sync.png'
TASK = _icon_path + 'task.png'
TASK_COMPLETED = _icon_path + 'task_completed.png'
TODAY = _icon_path + 'today.png'
TOMORROW = _icon_path + 'tomorrow.png'
TRASH = _icon_path + 'trash.png'
UPCOMING = _icon_path + 'upcoming.png'
VISIBLE = _icon_path + 'visible.png'

APP = _icon_path + 'app.png'
COPY = _icon_path + 'copy.png'
ICON = _icon_path + 'icon.png'
NEXT = _icon_path + 'next.png'
HEART = _icon_path + 'heart.png'
