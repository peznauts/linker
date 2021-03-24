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

from linker import APP


def start_app_debug():
    """Start the application in debug mode."""

    APP.run(debug=True)


def start_app_prod():
    """Start the application in production mode."""

    return APP


def db_sync():
    """Run DB sync to create the database."""

    from linker import db

    db.init_db()
