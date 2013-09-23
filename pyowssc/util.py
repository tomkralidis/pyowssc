# -*- coding: ISO-8859-15 -*-
# =================================================================
#
# Authors: Tom Kralidis <tomkralidis@gmail.com>
#
# Copyright (c) 2011 Tom Kralidis
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

def datetime2iso(dt):
    ''' Return a time representation as ISO8601

    Arguments
    ---------
    dt: datetime object

    Returns: ISO8601 timestamp

    ''' 
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')

def bindURL(url):
    ''' binds an HTTP GET query string

    Arguments
    ---------
    url: base URL of server

    Returns: url prepared for query string

    '''

    if url.find('?') == -1:  # like http://host/wms
        return '?'

    # if like http://host/wms?foo=bar& or http://host/wms?foo=bar
    if url.find('=') != -1:
        if url.find('&', -1) != -1:  # like http://host/wms?foo=bar&
            return ''
        else:  # like http://host/wms?foo=bar
            return '&'

    # if like http://host/wms?foo
    if url.find('?') != -1:
        if url.find('?', -1) != -1:  # like http://host/wms?
            return ''
        elif url.find('&', -1) == -1:  # like  http://host/wms?foo=bar
            return '&'
