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

import base64
import hashlib
import os
import re
import urllib.parse

import flask
from flask import request

from linker import APP
from linker.db import DB_SESSION
from linker.models import Link


CACHE_HEADERS = {
    'X-Frame-Options': 'SAMEORIGIN',
    "Cache-Control": 'public, max-age=120'
}


def _add_headers(headers_obj):
    """Insert headers from our CACHE_HEADERS constant.

    :headers_obj: Object

    :returns: Object
    """

    for key, value in CACHE_HEADERS.items():
        headers_obj[key] = value

    for k, v in APP.config['LINKER_DONATE'].items():
        headers_obj['X-Donate-{}'.format(k)] = v

    return headers_obj


def _response_text_format(response, link=None):
    """Add response headers.

    :response: Object
    :link: String

    :returns: Object
    """

    response.headers['Content-Type'] = 'text/plain; charset="utf-8"'
    response.headers = _add_headers(response.headers)
    if link:
        response.headers['X-Rendered-Link'] = link

    return response


def _base64encode(obj):
    """Return a base64 encoded object.

    :returns: Bytes
    """

    return base64.b64encode(str.encode(obj))


@APP.teardown_appcontext
def shutdown_session(*args, **kwargs):  # noqa
    """Close an SQL session."""

    DB_SESSION.remove()


@APP.route('/', methods=['GET'])
def index():
    """Site Index."""

    args = request.query_string.decode()
    if args:
        # Extract the link
        p = re.compile('link=(.*)')
        result = p.search(args)
        try:
            link_parse = result.group(1).strip()
            link_parsed = urllib.parse.urlparse(link_parse)
        except AttributeError:
            flask.abort(400)
        # If the link provided has no scheme, add a basic one.
        if not link_parsed.scheme:
            link_parse = 'http://' + link_parsed.path

        link_content = _base64encode(link_parse)

        # Hash the link
        hash_object = hashlib.sha1(link_content)
        hex_dig = hash_object.hexdigest()
        if Link.query.filter(Link.sha1 == hex_dig).first():
            hashed_link = urllib.parse.urljoin(request.base_url, hex_dig)
        else:
            hashed_link = urllib.parse.urljoin(request.base_url, hex_dig)
            # Store in DB
            link_item = Link(
                content=link_content,
                sha1=hex_dig,
                user_agent=request.user_agent.string,
                ip=_base64encode(request.remote_addr),
                count=0
            )
            DB_SESSION.add(link_item)
            DB_SESSION.commit()

        return _response_text_format(
            response=flask.make_response(
                hashed_link
            ),
            link=hashed_link
        )

    return _response_text_format(
        response=flask.make_response(
            APP.config['LINKER_BASIC_USAGE'].format(
                url=request.base_url.rstrip('/')
            )
        )
    )


@APP.route('/stats', methods=['GET'])
def stats():
    """Render the statistics page."""

    response = flask.make_response(
        flask.render_template(
            'index.html',
            remote_url=request.base_url,
            count=Link.query.count(),
            links=[
                (
                    i.sha1,
                    base64.b64decode(i.content).decode(),
                    i.count
                ) for i in Link.query.order_by(Link.count.desc()).limit(20)
            ]
        )
    )
    response.headers = _add_headers(response.headers)
    return response


@APP.route('/<link_id>', methods=['GET', 'HEAD'])
def get_link(link_id):
    """Site link.

    :link_id: String
    """

    try:
        if len(link_id) != 40:
            raise ValueError('Invalid SHA1')
        int(link_id, 16)
    except ValueError:
        flask.abort(400)
    else:
        q = Link.query.filter(Link.sha1 == link_id).first()
        if q:
            redirect = base64.b64decode(q.content).decode()
            return_headers = {
                'Referer': request.base_url,
                'Referrer-Policy': 'unsafe-url',
                'X-Link-Used': q.count
            }
            return_headers = _add_headers(headers_obj=return_headers)

            if request.method == 'GET':
                q.count += 1
                DB_SESSION.commit()

            return flask.redirect(redirect, code=308), return_headers
        else:
            flask.abort(404)


@APP.route('/robots.txt', methods=['GET'])
def robots():
    """Return robots response."""

    return _response_text_format(
        response=flask.make_response(
            flask.render_template('robots.txt'),
            200
        )
    )


@APP.route('/favicon.ico')
def favicon():
    """Return favicon response."""

    return flask.send_from_directory(
        os.path.join(
            APP.root_path,
            'static'
        ),
        'favicon.ico',
        mimetype='image/x-icon'
    )
