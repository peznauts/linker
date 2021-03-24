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

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import LargeBinary
from sqlalchemy import String

from linker.db import BASE


class Link(BASE):
    """Link table.

    Storage table for link content. All links stored are encoded in Binary
    format with an accompanying SHA1, information about the user-agent and
    the originating IP address.
    """

    __tablename__ = "links"
    id = Column(Integer, primary_key=True)
    sha1 = Column(String(40), unique=True)
    content = Column(LargeBinary, unique=False)
    user_agent = Column(String(360), unique=False)
    ip = Column(LargeBinary, unique=False)
    count = Column(Integer, unique=False)

    def __init__(
        self, content=None, sha1=None, user_agent=None, ip=None, count=None
    ):
        self.content = content
        self.sha1 = sha1
        self.user_agent = user_agent
        self.ip = ip
        self.count = count

    def __repr__(self):
        return "<Link %r>" % (self.sha1)
