"""
Generate random text.

Note that this isn't really "lorem ipsum" because no effort is made to apply
grammatical rules to the words.
"""
import random

WORDS = ("adipisci aliquam amet consectetur dolor dolore dolorem eius est et"
         "incidunt ipsum labore magnam modi neque non numquam porro quaerat qui"
         "quia quisquam sed sit tempora ut velit voluptatem").split()


class RandomText():
    def __init__(self):
        self.words = WORDS
        self.sentence_word_range = (4, 12)
        self.paragraph_sentence_range = (3, 8)
        self.text_paragraph_range = (2, 5)

    def word(self):
        w = random.choice(self.words)
        return w

    def sentence(self, number_words=None):
        if not number_words:
            number_words = random.randint(*self.sentence_word_range)
        s = ' '.join(self.word() for _ in range(number_words))
        return s[0].upper() + s[1:] + '.'

    def paragraph(self, number_sentences=None):
        if not number_sentences:
            number_sentences = random.randint(*self.paragraph_sentence_range)
        p = ' '.join(self.sentence() for _ in range(number_sentences))
        return p

    def text(self, number_paragraphs=None):
        if not number_paragraphs:
            number_paragraphs = random.randint(*self.text_paragraph_range)
        t = '\n\n'.join(self.paragraph() for _ in range(number_paragraphs))
        return t


def sentence():
    return RandomText().sentence()


def paragraph():
    return RandomText().paragraph()
