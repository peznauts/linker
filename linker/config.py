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

import os
import uuid

# Database connection

# NOTE(cloudnull): To set your database to an externally hosted server set
#                  this constant accordingly. This can be set internally at
#                  /etc/linker/linker.conf.py
#
# Example: LINKER_DB = 'mysql+pymysql://user:password@database-host/db-name'
LINKER_DB = os.environ.get("LINKER_DB", "sqlite:////tmp/linker.db")

# Basic on screen return information from the API
LINKER_BASIC_USAGE = os.environ.get(
    "LINKER_BASIC_USAGE",
    """To create a simplified link use the following syntax:

{url}?link=https://peznauts.com

All returned links respond to GET and HEAD requests.

For statistics information visit {url}/stats
""",
)

# Add-in crypto donation headers to your site
#
# LINKER_DONATE = {
#     'BTC': 'xxx',
#     'TXZ': 'xxx'
# }
#
# If set to an environment variable, the option is defined as a comma
# separated k=v pair.
#
LINKER_DONATE = os.environ.get("LINKER_DONATE", dict())
if isinstance(LINKER_DONATE, str):
    dontate = dict()
    for item in LINKER_DONATE.split(","):
        for k, v in item.split("="):
            dontate[k.strip()] = v.strip()
    LINKER_DONATE = dontate


# Google web analytics. Insert your user IDs using the following constants.
GOOGLE_ANALYTICS = os.environ.get("GOOGLE_ANALYTICS")
GOOGLE_ADSENSE = os.environ.get("GOOGLE_ADSENSE")

# Flask-sqlalchemy options
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
}
# Ff you don't override the secret key, one will be chosen for you
SECRET_KEY = uuid.uuid4().hex

# System options
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
