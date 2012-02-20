#!/usr/bin/env python
"""
Test suit
"""
__author__ = "Tirino"

import scrapydo
import unittest

class TestBrowserFunctions(unittest.TestCase):
    # pylint: disable-msg=R0904
    """
    Test case for some of the browser functions of scrapydo
    """
    def setUp(self):
        """
        Set up an instance of ScrapyDo
        """
        # pylint: disable-msg=C0103
        self.scrapy = scrapydo.ScrapyDo()

    def test_url_as_string(self):
        """
        Check that we can properly download Slashdot's home page as a string
        """
        needle = '<title>Slashdot: News for nerds, stuff that matters</title>'
        bad_needle = '<title>reddit: the front page of the internet</title>'
        haystack = self.scrapy.get_url_content('http://slashdot.org')
        self.assertTrue(needle in haystack)
        self.assertFalse(bad_needle in haystack)

    def test_url_as_soup(self):
        """
        Check that we can properly download Slashdot's home page as an object
        """
        needle = u'Slashdot: News for nerds, stuff that matters'
        page = self.scrapy.get_url_as_soup('http://slashdot.org')
        self.assertIsNotNone(page)

        title = page.find('title')
        self.assertIsNotNone(title)
        self.assertEqual(title.name, 'title')
        self.assertEqual(title.contents, [needle])

if __name__ == '__main__':
    unittest.main()
