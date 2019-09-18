"""
Unit tests for the generators.text module.

"""

from pip._vendor.pyparsing import basestring

from datagen.generators.text import RandomText, sentence, paragraph


def test_word():
    rt = RandomText()
    assert isinstance(rt.word(), basestring)


def test_sentence():
    rt = RandomText()
    assert rt.sentence()[0].isupper()
    assert sentence().endswith('.')
    assert len(rt.sentence(11).split(' ')) == 11


def test_paragraph():
    rt = RandomText()
    assert paragraph()[0].isupper()
    assert paragraph().endswith('.')
    assert len(rt.paragraph().split(' ')) > 12


def test_text():
    rt = RandomText()
    assert len(rt.text().split(' ')) > 24
