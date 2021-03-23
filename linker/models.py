from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import LargeBinary

from linker.db import Base


class Link(Base):
    """Link table.

    Storage table for link content. All links stored are encoded in Binary
    format with an accompanying SHA1, information about the user-agent and
    the originating IP address.
    """

    __tablename__ = 'links'
    id = Column(Integer, primary_key=True)
    sha1 = Column(String(40), unique=True)
    content = Column(LargeBinary, unique=False)
    user_agent = Column(String(360), unique=False)
    ip = Column(LargeBinary, unique=False)
    count = Column(Integer, unique=False)

    def __init__(self, content=None, sha1=None, user_agent=None, ip=None,
                 count=None):
        self.content = content
        self.sha1 = sha1
        self.user_agent = user_agent
        self.ip = ip
        self.count = count

    def __repr__(self):
        return '<Link %r>' % (self.sha1)
