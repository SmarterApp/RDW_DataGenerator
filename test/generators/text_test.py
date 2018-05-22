"""
Unit tests for the generators.text module.

"""

from nose.tools import *
from pip._vendor.pyparsing import basestring

from data_generator.generators.text import RandomText, sentence, paragraph


def test_word():
    rt = RandomText()
    assert_is_instance(rt.word(), basestring)


def test_sentence():
    rt = RandomText()
    assert_true(rt.sentence()[0].isupper())
    assert_true(sentence().endswith('.'))
    assert_true(len(rt.sentence(11).split(' ')) == 11)


def test_paragraph():
    rt = RandomText()
    assert_true(paragraph()[0].isupper())
    assert_true(paragraph().endswith('.'))
    assert_true(len(rt.paragraph().split(' ')) > 12)


def test_text():
    rt = RandomText()
    assert_true(len(rt.text().split(' ')) > 24)
