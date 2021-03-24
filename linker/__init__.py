#   Copyright Peznauts <kevin@cloudnull.com>. All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

import logging
import logging.handlers

import flask


APP = flask.Flask(__name__, instance_relative_config=True)


def _app_setup():
    """start the application."""

    APP.config.from_object("linker.config")
    APP.config.from_pyfile("/etc/linker/linker.conf.py", silent=True)

    try:
        APP.config.from_envvar("LINKER_SETTINGS", silent=True)
    except RuntimeError:
        pass

    if APP.debug:
        formatter = logging.Formatter(
            fmt=(
                "[%(asctime)s.%(msecs)03d]"
                " pid=%(process)d %(levelname)s: %(message)s"
            ),
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        for handler in APP.logger.handlers:
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(formatter)

    APP.config["APP_SETUP"] = True


if not APP.config.get("APP_SETUP"):
    _app_setup()
    import linker.views as views  # noqa
