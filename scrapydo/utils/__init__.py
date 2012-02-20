#!/usr/bin/env python
"""
Asorted utility functions
"""
__author__ = "Tirino"

import re
from abc import ABCMeta, abstractmethod

class BrowserGenerator:
    # pylint: disable-msg=W0232
    """
    Abstract class to be subclassed by the user to generate its own browser
    information
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def extra_headers(self):
        """
        Return a list of headers to be appended to each 'browser' request
        Each header should be a tuple in the format:
            ('Header-Name', 'headervalue')
        """
        pass

    @abstractmethod
    def get_user_agent(self):
        """
        Return the value to be used for the User-Agent header
        """
        pass

    @abstractmethod
    def get_accept_lang(self):
        """
        Return the value to be used for the Accept-Language header
        """
        pass


def remove_bom(text):
    """
    Removes the BOM from a string
    """
    return text.replace('\xef', '').replace('\xbb', '').replace('\xbf', '')

def titlecase(text):
    """
    Similar to string.title() but with some improvements.
    """
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
            lambda  mo: mo.group(0)[0].upper() +
                    mo.group(0)[1:].lower(),
            text)
