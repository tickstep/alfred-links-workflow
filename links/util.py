from datetime import date, datetime, timedelta
import logging

from workflow import Workflow

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

_workflow = None
_update_settings = None


def workflow():
    global _workflow, _update_settings

    if _workflow is None:
        version = '0.1.2'

        _workflow = Workflow(
            capture_args=False,
            update_settings={
                'github_slug': 'tickstep/alfred-links-workflow',
                'version': version,
                # Check for updates daily
                # TODO: check less frequently as the workflow becomes more
                # stable
                'frequency': 1,
                # Always download pre-release updates if a prerelease is
                # currently installed
                'prerelease': '-' in version
            }
        )

        # Avoid default logger output configuration
        _workflow.logger = logging.getLogger('workflow')

    return _workflow


def relaunch_alfred(command='lk '):
    import subprocess

    alfred_major_version = workflow().alfred_version.tuple[0]

    subprocess.call([
        '/usr/bin/env', 'osascript', '-l', 'JavaScript',
        'bin/launch_alfred.scpt', command, str(alfred_major_version)
    ])


def utc_to_local(utc_dt):
    import calendar
    
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    return local_dt.replace(microsecond=utc_dt.microsecond)
