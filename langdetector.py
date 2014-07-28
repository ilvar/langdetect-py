#!/usr/bin/env python

import re
import nltk  # will be used only for tokenizing so everything else will work even without this module
import string


class LanguageDetector(object):
    """
    Detects language of documents based on provided dictionaries (i.e. from /usr/share/dict/).
    """

    def __init__(self, dict_files):
        """
        Read dictionaries, initialize detector.

        :param dict_files: Dictionary of "language  label" -> "path/to/dictionary"
        :type dict_files: dict.

        """

        self.FOUND_THRESHOLD = 100  # if found 100 words - skip rest of a document

        self.dictionaries = {}
        for label, path in dict_files.items():
            f = open(path, 'r')
            # converting strings to lower case, stripping newlines
            self.dictionaries[label] = frozenset(map(string.lower, map(string.strip, f.readlines())))

        self.re_splitter = re.compile('[^\w]')  # maybe manually filling up with string.punctuation will be faster

    def detect(self, words_set):
        """
        Detect probable language of a document.

        :param words_set: Text of a document split into words and loaded into a set
        :type words_set: set.

        :returns: basestring -- language label

        """
        weights = [(k, len(words_set.intersection(d))) for k, d in self.dictionaries.items()]
        probable_lang = max(weights, key=lambda w: w[1])  # need to get most probable language

        # We can return all languages with their probabilities if necessary
        return probable_lang

    def detect_split_string(self, document):
        """
        Detect using built-in .split() for document. Should be the fastest, but will
        drop some words with punctuation around.

        :param document: Text of a document
        :type document: basestring.

        :returns: basestring -- language label

        """

        words_set = frozenset(document.lower().split())
        return self.detect(words_set)

    def detect_split_re(self, document):
        """
        Detect using split with regular expressions.

        :param document: Text of a document
        :type document: basestring.

        :returns: basestring -- language label

        """

        words_set = frozenset(re.split(self.re_splitter, document.lower()))
        return self.detect(words_set)

    def detect_split_nltk(self, document):
        """
        Detect using split from `nltk` module. Should be the most reliable but slowest.

        :param document: Text of a document
        :type document: basestring.

        :returns: basestring -- language label

        """

        words_set = frozenset(nltk.word_tokenize(document.lower()))
        return self.detect(words_set)

if __name__ == '__main__':
    import timeit

    print 'Performance measures:'  # Not necessary in production, just wanted to compare implementations.

    ld = LanguageDetector({'british': './british.dict', 'spanish': './spanish.dict'})
    british_doc = open('british_doc.txt', 'r').read()
    spanish_doc = open('spanish_doc.txt', 'r').read()

    print 'British'
    print 'Built-in strings', sum(timeit.repeat(lambda: ld.detect_split_string(british_doc), number=10))
    print 'Regular expressions', sum(timeit.repeat(lambda: ld.detect_split_re(british_doc), number=10))
    print 'Python NLTK', sum(timeit.repeat(lambda: ld.detect_split_nltk(british_doc), number=10))

    print 'Spanish'
    print 'Built-in strings', sum(timeit.repeat(lambda: ld.detect_split_string(spanish_doc), number=10))
    print 'Regular expressions', sum(timeit.repeat(lambda: ld.detect_split_re(spanish_doc), number=10))
    print 'Python NLTK', sum(timeit.repeat(lambda: ld.detect_split_nltk(spanish_doc), number=10))

"""
    Performance measures showed than NLTK tokenizer is the slowest (nearly 10 times slower than RegExp),
    re's are 2 times slower than string splitter. But string splitter misses ~10% of words.

    If documents are big enough, we can use string splitter freely, for smaller documents NLTK would be
    more reliable. It is possibly good to use the same approach as in Python's built-in `sort` function,
    which uses memory-efficient Insertion sort for small datasets and processor-efficient Merge sort for
    larger sets.
"""