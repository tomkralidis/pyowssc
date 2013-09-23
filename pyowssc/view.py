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

from lxml import etree

from pyowssc import util

class Xml(object):
    ''' XML marshalling '''

    def __init__(self, encoding='UTF-8', pretty_print=True):
        ''' initialize core properties '''

        self.encoding = encoding
        self.pretty_print = pretty_print
        self.namespaces = {
           None: 'http://registry.gsdi.org/statuschecker/services/rest/',
           'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }
   
    def encode(self, model, requesttype='full'):
        ''' output service object as XML '''
    
        response = etree.Element('response', nsmap=self.namespaces)
        response.attrib['{%s}schemaLocation' % self.namespaces['xsi']] = '%s %sresponseSchema.xsd' % (self.namespaces[None], self.namespaces[None])
            
        service = etree.SubElement(response, 'service')
        service.attrib['type'] = model.type
        service.attrib['date'] = model.date
            
        summary = etree.SubElement(service, 'summary')
            
        providedurl = etree.SubElement(summary, 'providedURL')
        providedurl.attrib['type'] = 'GetCapabilities'
        providedurl.attrib['validity'] = '1'
        providedurl.text = model.tests['GetCapabilities']['url']
            
        scoredtest = etree.SubElement(summary, 'scoredTest')
        scoredtest.attrib['type'] = 'GetCapabilities'
            
        performance1 = etree.SubElement(scoredtest, 'performance')
        performance1.attrib['type'] = 'currentSpeed'
        performance1.text = model.tests['GetCapabilities']['currentSpeed']
            
        performance2 = etree.SubElement(scoredtest, 'performance')
        performance2.attrib['type'] = 'currentScore'
        performance2.text = model.tests['GetCapabilities']['currentScore']

        if requesttype == 'full':
            test = etree.SubElement(service,'test')
            test.attrib['type'] = 'httpServer'
            test.attrib['startTime'] = util.datetime2iso(model.tests['httpServer']['startTime'])
            test.attrib['endTime'] = util.datetime2iso(model.tests['httpServer']['endTime'])

            input = etree.SubElement(test, 'input')
            input.attrib['type'] = 'URL'

            input.text = model.tests['httpServer']['url']

            output = etree.SubElement(test, 'output')
            output.attrib['type'] = 'success'
            output.text = model.tests['httpServer']['output']['success']
        
            if model.tests['httpServer']['output']['success'] == '0':  
                output2 = etree.SubElement(test, 'output')
                output2.attrib['type'] = 'error'
                output2.text = model.tests['httpServer']['output']['message']

            test2 = etree.SubElement(service,'test')
            test2.attrib['type'] = 'GetCapabilities'
            test2.attrib['startTime'] = util.datetime2iso(model.tests['GetCapabilities']['startTime'])
            test2.attrib['endTime'] = util.datetime2iso(model.tests['GetCapabilities']['endTime'])

            input = etree.SubElement(test2, 'input')
            input.attrib['type'] = 'URL'

            input.text = model.tests['GetCapabilities']['url']

            output = etree.SubElement(test2, 'output')
            output.attrib['type'] = 'success'
            output.text = model.tests['GetCapabilities']['output']['success']

            if model.tests['GetCapabilities']['output']['success'] == '0':
                output2 = etree.SubElement(test2, 'output')
                output2.attrib['type'] = 'error'
                output2.text = model.tests['GetCapabilities']['output']['message']

        return etree.tostring(response, xml_declaration=True, encoding=self.encoding, pretty_print=self.pretty_print)
