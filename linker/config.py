import uuid

# Local temp directory
LINKER_DIR = '/tmp/linker'

# Database connection

# NOTE(cloudnull): To set your database to an externally hosted server set this
#                  constant accordingly. This can be set internally at
#                  /etc/linker/linker.conf.py
#
# Example: LINKER_DB = 'mysql+pymysql://user:password@database-host/database-name'
LINKER_DB = 'sqlite:////tmp/linker.db'

# Web analytics
GOOGLE_ANALYTICS = None
GOOGLE_ADSENSE = None

# if you don't override the secret key, one will be chosen for you
SECRET_KEY = uuid.uuid4().hex
WTF_CSRF_ENABLED = False

# System options
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE='Lax'

# Basic on screen return information from the API
LINKER_BASIC_USAGE = """To create a simplified link use the following syntax:

{url}?link=https://peznauts.com"

All returned links respond to GET and HEAD requests.

For statistics information visit {url}/stats
"""
