#!/usr/bin/env python
# encoding: utf-8

# Copyright (c) 2016 Peter Teichman
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from collections import namedtuple
import re

__all__ = ["quotefix", "quotefix_skip"]

Token = namedtuple("Token", "type char")
fwdchars = u'({[“"'
revchars = u')}]”"'


class TokenType:
    Literal = "Literal"
    Open = "Open"
    Close = "Close"


def quotefix(text):
    """quotefix inserts matching punctuation for mismatched quotes etc"""
    def false(text):
        return False
    return quotefix_skip(text, false)


def quotefix_skip(text, skipfunc):
    """quotefix_skip inserts matching punctuation, skipping words if needed"""
    tokens = []

    words = re.findall("(\s+|\S+)", text, re.UNICODE)
    for word in words:
        if skipfunc(word):
            tokens.extend(literals(word))
        else:
            tokens.extend(quotetokens(word))

    return "".join(token.char for token in fixrev(fixfwd(tokens)))


def quotetokens(word):
    ret = []
    for i, c in enumerate(word):
        if c == '"':
            d = direction(word, i)
            ret.append(Token(type=d, char=c))
        elif c in fwdchars:
            ret.append(Token(type=TokenType.Open, char=c))
        elif c in revchars:
            ret.append(Token(type=TokenType.Close, char=c))
        else:
            ret.append(Token(type=TokenType.Literal, char=c))

    return ret


def literals(word):
    return [Token(type=TokenType.Literal, char=c) for c in word]


def mirror(c):
    i = fwdchars.find(c)
    if i >= 0:
        return revchars[i]

    i = revchars.find(c)
    if i >= 0:
        return fwdchars[i]

    return c


def direction(word, pos):
    """Direction returns the direction (open/close) of a quote char at pos"""
    if pos < len(word)/2:
        return TokenType.Open
    return TokenType.Close


def fixfwd(tokens):
    """fixfwd inserts close tokens for unmatched opens."""
    stack = []
    prev = None

    ret = []
    for t in tokens:
        if t.type == TokenType.Open:
            stack.append(t.char)
        elif stack and t.type == TokenType.Close:
            prev = stack.pop()
            if prev != mirror(t.char):
                ret.append(Token(type=TokenType.Close, char=mirror(prev)))
        ret.append(t)

    while stack:
        prev = stack.pop()
        ret.append(Token(type=TokenType.Close, char=mirror(prev)))

    return ret


def fixrev(tokens):
    """fixrev inserts open tokens for unmatched closes."""
    stack = []
    prev = None

    ret = []
    for t in reversed(tokens):
        if t.type == TokenType.Close:
            stack.append(t.char)
        elif stack and t.type == TokenType.Open:
            prev = stack.pop()
            if prev != mirror(t.char):
                ret.append(Token(type=TokenType.Open, char=mirror(prev)))
        ret.append(t)

    while stack:
        prev = stack.pop()
        ret.append(Token(type=TokenType.Open, char=mirror(prev)))

    return reversed(ret)
