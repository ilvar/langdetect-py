langdetect-py
=============

Language detection with ispell dictionaries

British english and Spanish dictionaries and documents (both are some random governmental-issued, converted to txt) are
included for testing and performance measurement.

Usage
-----

The only requirement now is NLTK, maybe we'll remove it in the future.

    from langdetector import LanguageDetector

    ld = LanguageDetector({"language_label": "/path/to/dictionary", "other_label": "/path/to/other/dictionary"})
    print 'Built-in', ld.detect_split_string(document_text) # for built-in string splitting
    print 'RegExp', ld.detect_split_re(document_text) # for regular expression splitting
    print 'NLTK', ld.detect_split_nltk(document_text) # for NTLTK splitting

Returned value is `tuple(language_label, found_words_count)`.

Testing
-------

To run functional tests use

    python tests.py

To run performance measurement use

    python langdetect.py

TODO
----

* Remove dictionaries and documents from the repository. Maybe test with random generated documents?
* Research if there is any use in NLTK. Maybe we can remove it completely?
* Create a `setuptools` package
