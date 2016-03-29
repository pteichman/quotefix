quotefix
========

This Python module inserts punctuation to balance quotation marks,
parentheses, and brackets that are unmatched in a Unicode string.

It allows you to use text synthesis techniques that are unaware of
these internal clauses and still clean things up nicely for
presentation.

Like this:

    >>> quotefix('She said, "I ran out (to the store')
    'She said, "I ran out (to the store)"'
    
    >>> quotefix("it works in reverse too)")
    '(it works in reverse too)'

You came here because you want to...

* Install the latest release: `pip install quotefix`
* Read the documentation: `pydoc quotefix`
* File a bug: https://github.com/pteichman/quotefix/issues
* Submit a change: file a pull request at https://github.com/pteichman/quotefix/pulls

Assumptions
===========

The main assumption made by quotefix is that punctuation ending a
nested clause (a parenthetic aside, a quotation, etc) should also end
any other open clauses. Likewise, punctuation opening a clause should
open any unopened clauses in the remainder of the string.

A secondary assumption concerns the direction of the double quotation
mark: ". If this character is closer to the beginning of a word, it's
assumed to be an open quote.

History
=======

quotefix started as a function in Fate, a fast & scalable trigram chat
framework: https://github.com/pteichman/fate
