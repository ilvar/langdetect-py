#!/usr/bin/env python

"""
I've put everything in one file, because code and tests are simple. In Django of course tests will be in separate module.
"""

import unittest

from langdetector import LanguageDetector


class LanguageDetectorTest(unittest.TestCase):
    def setUp(self):
        self.ld = LanguageDetector({'british': './british.dict', 'spanish': './spanish.dict'})
        self.british_doc = open('british_doc.txt', 'r').read()
        self.spanish_doc = open('spanish_doc.txt', 'r').read()

    def test_init(self):
        self.assertTrue(self.ld.dictionaries)
        self.assertSetEqual(set(self.ld.dictionaries.keys()), set(['british', 'spanish']))

    def test_simple(self):
        self.assertEqual(self.ld.detect_split_string(self.british_doc)[0], 'british')
        self.assertEqual(self.ld.detect_split_string(self.spanish_doc)[0], 'spanish')

    def test_re(self):
        self.assertEqual(self.ld.detect_split_re(self.british_doc)[0], 'british')
        self.assertEqual(self.ld.detect_split_re(self.spanish_doc)[0], 'spanish')

    def test_nltk(self):
        try:
            import nltk
        except ImportError:
            # If NLTK is not installed, just skip it
            print 'NLTK is not installed'
        else:
            self.assertEqual(self.ld.detect_split_nltk(self.british_doc)[0], 'british')
            self.assertEqual(self.ld.detect_split_nltk(self.spanish_doc)[0], 'spanish')


if __name__ == '__main__':
    unittest.main()
