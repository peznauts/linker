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

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from linker import APP


ENGINE = create_engine(
    APP.config["LINKER_DB"], convert_unicode=True, pool_recycle=1800
)
DB_SESSION = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
)
BASE = declarative_base()
BASE.query = DB_SESSION.query_property()


def init_db():
    """Initialize the database."""

    BASE.metadata.create_all(bind=ENGINE)
