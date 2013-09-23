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

import socket
import StringIO
import urllib2
import urlparse
import datetime
from lxml import etree

from pyowssc import util

class Service(object):
    ''' Base service class '''

    def __init__(self, type, url):
        ''' initialize '''
        self.type = type
        self.url = url
        self.date = util.datetime2iso(datetime.datetime.now())
        self.tests = {}

    def test(self):
        ''' run the test '''

        test = {}
        test['startTime'] = datetime.datetime.now()
        test['input'] = {}
        test['output'] = {}
        test['input']['type'] = 'URL'

        # test http ping

        u = urlparse.urlsplit(self.url)

        if u.port is None:
            port = 80
            test['url'] = 'http://%s' % u.netloc
        else:
            port = u.port
            test['url'] = 'http://%s:%s' % (u.netloc, u.port)

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((u.netloc, port))
        except socket.error, msg:
            test['output']['success'] = '0'
            test['output']['type'] = 'error'
            test['output']['message'] = str(msg)
            test['currentSpeed'] = '-99.99'
            test['currentScore'] = '-99.99'
            test['endTime'] = datetime.datetime.now()
        else:
            test['output']['success'] = '1'
            test['output']['type'] = 'success'
            test['endTime'] = datetime.datetime.now()
            delta = test['endTime'] - test['startTime']
            deltafmt = '%s.%s' % (delta.seconds, delta.microseconds)
            test['currentSpeed'] = deltafmt
            test['currentScore'] = '100.00'

        self.tests['httpServer'] = test

        # test GetCapabilities

        test = {}
        test['startTime'] = datetime.datetime.now()
        test['input'] = {}
        test['output'] = {}

        test['url'] = '%s%sversion=1.1.1&service=WMS&request=GetCapabilities' % (self.url, util.bindURL(self.url))

        try:
            response = urllib2.urlopen(test['url'])
        except urllib2.URLError, e: # HTTP error
            test['output']['success'] = '0'
            test['output']['type'] = 'error'
            if hasattr(e, 'code'):
                test['output']['message'] = str(e.code)
            elif hasattr(e, 'reason'):
                test['output']['message'] = str(e.reason)
            test['currentSpeed'] = '-99.99'
            test['currentScore'] = '-99.99'
        else:
            # test if it's an actual XML document
            try:
                content = etree.parse(StringIO.StringIO(response.read()))
            except etree.XMLSyntaxError, e:
                test['output']['success'] = '0'
                test['output']['type'] = 'error'
                test['output']['message'] = str(e)
                test['currentSpeed'] = '-99.99'
                test['currentScore'] = '-99.99'
            else:
                root = content.getroot().tag
                test['output']['type'] = 'success'
                # test that it's Capabilities XML
                if root == 'WMT_MS_Capabilities' or root == 'WMS_Capabilities':
                    test['output']['success'] = '1'
                else:
                    test['output']['success'] = '0'
                    if content.find('ServiceException') is not None:
                        test['output']['message'] = content.find('ServiceException').text
                    else:
                        test['output']['message'] = 'Unrecognized Capabilities XML'
    
                test['currentScore'] = '100.00'
    
        test['endTime'] = datetime.datetime.now()
        delta = test['endTime'] - test['startTime']
        deltafmt = '%s.%s' % (delta.seconds, delta.microseconds)
        test['currentSpeed'] = deltafmt
        self.tests['GetCapabilities'] = test
