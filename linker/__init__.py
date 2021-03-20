import logging
import logging.handlers
import os

import flask

app = flask.Flask(__name__, instance_relative_config=True)


def _app_setup():
    """start the application."""

    app.config.from_object('linker.config')

    app.config.from_pyfile('/etc/linker/linker.conf.py', silent=True)

    try:
        app.config.from_envvar('LINKER_SETTINGS', silent=True)
    except RuntimeError:
        pass

    # ensure the local LINKER_DIR exists
    _local_path = os.path.expanduser(app.config['LINKER_DIR'])
    if not os.path.exists(_local_path):
        os.mkdir(path=_local_path)

    if app.debug:
        formatter = logging.Formatter(
            fmt='[%(asctime)s.%(msecs)03d] pid=%(process)d %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

        for handler in app.logger.handlers:
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(formatter)

    app.config['APP_SETUP'] = True


if not app.config.get('APP_SETUP'):
    _app_setup()
    import linker.views as views # flake8: noqa

