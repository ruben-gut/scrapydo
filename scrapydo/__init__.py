#!/usr/bin/env python
"""
Scrapy-Do main package
"""
__author__ = "Tirino"

# system
import re
import urllib
import cookielib
import sys
# third party
import mechanize
from BeautifulSoup import BeautifulSoup

DEFAULT_HTTP_USER_AGENT = "%s%s%s" % ('Mozilla/5.0 (Macintosh; U; Intel ',
                        'Mac OS X 10_6_6; en-us) AppleWebKit/533.19.4 ',
                        '(KHTML, like Gecko) Version/5.0.3 Safari/533.19.4')

DEFAULT_HTTP_ACCEPT_LANGUAGE = 'en-us;q=0.7,en;q=0.3'
HTTP_GENERIC_ERROR = 'HTTP Error'

HTTP_FILE_NOT_FOUND = '404'
HTTP_SERVER_ERRORS = ['503', '502', '501', '500']


class TemporaryErrorException(Exception):
    """
    Raised when the remote server is having temporary problems
    Usually when it returns Error 503.
    """
    pass

class FileNotFoundException(Exception):
    """
    Raised when a file is not found on the remote server.
    """
    pass

def parse_exception(ex, data):
    """
    Take a generic exception and tries to return one that says
    more about the error, such as "FileNotFoundException".
    """
    result = ex
    error_msg = str(ex)
    if HTTP_GENERIC_ERROR in error_msg:
        if HTTP_FILE_NOT_FOUND in error_msg:
            result = FileNotFoundException("File Not Found: %s" % data)
        else:
            for error_number in HTTP_SERVER_ERRORS:
                if error_number in error_msg:
                    result = TemporaryErrorException("Server error: %s" % ex)
    return result

class ScrapyDo(object):
    """
    Handle connecting to a remote server and doing
    generic stuff.
    """
    def __init__(self, browser_generator=None):
        """
        Initialize browser support
        """
        # Init Browser
        self.browser = mechanize.Browser()
        self.browser_generator = browser_generator
        self.user_agent = DEFAULT_HTTP_USER_AGENT
        self.accept_lang = DEFAULT_HTTP_ACCEPT_LANGUAGE

        headers = []
        if self.browser_generator:
            headers = self.browser_generator.extra_headers()
            self.user_agent = self.browser_generator.get_user_agent()
            self.accept_lang = self.browser_generator.get_accept_lang()

        headers.append(('User-Agent', self.user_agent))
        headers.append(('Accept-Language', self.accept_lang))

        self.browser.addheaders = headers
        self.browser.set_handle_robots(False)

        # Enable Cookies
        self.cookie_jar = cookielib.LWPCookieJar()
        self.browser.set_cookiejar(self.cookie_jar)

    def get_url_content(self, url):
        """
        Call an URL and return its content as a string
        """
        # pylint: disable-msg=E1102
        return self.browser.open(url).read()

    def get_url_as_soup(self, url):
        """
        Call an URL and return its content as a BeautifulSoupe object
        Documentation:
        http://www.crummy.com/software/BeautifulSoup/bs3/documentation.html
        """
        return BeautifulSoup(self.get_url_content(url))

    def do_ajax_request(self, url, params , referer=None):
        """
        Simulate an ajax request
        """
        # Do an Ajax call simulating the browser
        # User mechanize.Request to send POST request
        req = mechanize.Request(url, urllib.urlencode(params))
        req.add_header('User-Agent', self.user_agent)
        req.add_header('X-Requested-With', 'XMLHttpRequest')
        req.add_header('Content-Type', 
                        'application/x-www-form-urlencoded; charset=UTF-8')
        if (referer):
            req.add_header('Referer', referer)

        # Use the same cookie jar we've been using
        self.cookie_jar.add_cookie_header(req)
        result = mechanize.urlopen(req)
        return result.read()

    def download_file(self, url, target):
        """
        Download the file at the specified URL and save it in the target
        location
        """
        # pylint: disable-msg=E1102
        try:
            self.browser.retrieve(url, filename=target)
        except KeyboardInterrupt, ex:
            # we may be downloading a large file so
            # we should cancel the download and exit
            sys.exit(0)
        except Exception, ex:
            new_ex = parse_exception(ex, url)
            raise new_ex # propagate the new exception

