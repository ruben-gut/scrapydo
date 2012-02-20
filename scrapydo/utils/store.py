#!/usr/bin/env python
"""
Code related to storing stuff. Unfinished.
"""
__author__ = "Tirino"

from abc import ABCMeta, abstractmethod

class Store:
    # pylint: disable-msg=W0232
    # pylint: disable-msg=R0903
    """
    Abstract base class for storing stuff downloaded with ScrapyDo
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def save(self, type_, item):
        """
        Persist a downloaded item
        """
        pass
