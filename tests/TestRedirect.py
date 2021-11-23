#!/usr/local/bin/python3.5
import unittest
import os
import sys
import requests
try:
    import urlparse
except:
    from urllib.parse import urlparse

class TestRedirect(unittest.TestCase):
    baseurl = ''
    desturl = ''
    def setUp(self):
        self.baseurl = os.environ["baseurl"]
        self.desturl = os.environ["desturl"]

    def checkOK(self, source, host):
        code = 0
        response = requests.get(source, allow_redirects=False, headers={'host': host})
        code = response.status_code
        self.assertEqual(code, 200, 'Failed to get 200 from host %s due to %s' % (host, code))

    def redirectCheck(self, url, target,host=None):
        code = 0
        if host:
            response = requests.get(url, allow_redirects=False, headers={'host': host})
        else:    
            response = requests.get(url, allow_redirects=False)

        code = response.status_code
        location = url
        if 'Location' in response.headers:
            location = response.headers['Location']
        self.assertEqual(code, 301, 'Failed to get redirected %s to %s due to %s' % (url, target, code))
        self.assertEqual(location, target, 'Failed to redirect to the correct place. Expected %s but got %s' % (target, location))

    def checkHeader(self, url, headers, host=None):
        code = 0
        if host:
            response = requests.get(url, allow_redirects=False, headers={'host': host})
        else:    
            response = requests.get(url, allow_redirects=False)

        for header in headers:
            self.assertIsNotNone(response.headers[header], 'Missing header {}'.format(header))
            self.assertEqual(headers[header], response.headers[header], 'Header missmatched. Expected {}, got {}'.format(headers[header], response.headers[header]))

    def test_checkImage(self):
        url = '%s/%s' % (self.baseurl, 'image/iiif/2/owl%2F20180608%2FIMG_0001/info.json')
        host = 'iiif.gdmrdigital.com'
        self.checkOK(url, host)

    def test_checkRedirect(self):
        url = '%s/%s' % (self.baseurl, 'image/iiif/2/owl%2F20180608%2FIMG_0001.jp2/info.json')
        target = 'http://iiif.gdmrdigital.com/%s' % ('image/iiif/2/owl%2F20180608%2FIMG_0001/info.json')
        host = 'iiif.gdmrdigital.com'
        self.redirectCheck(url, target, host)

    def test_checkCORS(self):
        url = '%s/%s' % (self.baseurl, 'image/iiif/2/mouse_brain%2FMD594-IHC1-2015.08.26-15.15.28_MD594_1_0001_lossy.jp2/info.json')
        host  = 'iiif.gdmrdigital.com'
        self.checkHeader(url, {
            "Access-Control-Allow-Origin": "*"
          }, host)



if __name__ == '__main__':
    baseurl = 'http://0.0.0.0'
    if len(sys.argv) == 2:
        baseurl = sys.argv[1]

    os.environ["baseurl"] = baseurl
    unittest.main()
