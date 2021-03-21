import os
import uuid

# Database connection

# NOTE(cloudnull): To set your database to an externally hosted server set this
#                  constant accordingly. This can be set internally at
#                  /etc/linker/linker.conf.py
#
# Example: LINKER_DB = 'mysql+pymysql://user:password@database-host/database-name'
LINKER_DB = os.environ.get('LINKER_DB', 'sqlite:////tmp/linker.db')

# Basic on screen return information from the API
LINKER_BASIC_USAGE = os.environ.get(
    'LINKER_BASIC_USAGE',
    """To create a simplified link use the following syntax:

{url}?link=https://peznauts.com

All returned links respond to GET and HEAD requests.

For statistics information visit {url}/stats
"""
)

# Google web analytics. Insert your user IDs using the following constants.
GOOGLE_ANALYTICS = os.environ.get('GOOGLE_ANALYTICS')
GOOGLE_ADSENSE = os.environ.get('GOOGLE_ADSENSE')
