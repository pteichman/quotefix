#!/usr/bin/env python
# encoding: utf-8

import re
import unittest

# Verify that __all__ is set properly in quotefix.
from quotefix import *


class TestQuotefix(unittest.TestCase):
    def test_basic(self):
        # (text, expected)
        tests = [
            (u"this is \"a test", u"this is \"a test\""),
            (u"\"this\" is \"a test", u"\"this\" is \"a test\""),
            (u"this) is \"a test", u"(this) is \"a test\""),
            (u"this)) is ((a test)", u"((this)) is ((a test))"),
            (u"this]) is ((a test)", u"([this]) is ((a test))"),
            (u"this” is “a test”", u"“this” is “a test”"),
            (u"(this is a test\"", u"\"(this is a test)\""),
        ]

        for text, expected in tests:
            fixed = quotefix(text)
            self.assertEqual(fixed, expected,
                "quotefix(%s) -> %s, want %s" % (text, fixed, expected))

    def test_skipfunc(self):
        def isemoticon(word):
            return re.match("[:;]-*[\(\)]+", word, re.UNICODE)

        tests = [
            (u"this is a test :)", u"this is a test :)"),
            (u":) :( :-) :-( ;)", u":) :( :-) :-( ;)"),
        ]

        for text, expected in tests:
            fixed = quotefix_skip(text, isemoticon)
            self.assertEqual(fixed, expected,
                "quotefix(%s) -> %s, want %s" % (text, fixed, expected))


if __name__ == "__main__":
    unittest.main()
