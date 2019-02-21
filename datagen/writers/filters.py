"""
Create output filters for data values that are specific to the SBAC project.
"""

import random

import datagen.config.cfg as cfg


def filter_yesno(val):
    """
    Filter a True/False value as Yes/No.

    @param val: The value to filter
    @returns: Yes or No if value is True or False respectively
    """
    return 'Yes' if val else 'No'


def filter_yesnoblank(val):
    """
    Filter a True/False value as Yes/No, but when no have a 8% chance that the value will be blank.

    @param val: The value to filter
    @returns: Yes or No if value is True or False respectively, but 8% of time 'No' will be blank.
    """
    return 'Yes' if val else 'No' if random.randint(1, 100) < 93 else ''


def filter_always_true(val):
    """
    Always return True.

    @param val: The value that is ignored
    @returns: True
    """
    return True


def filter_only_delete(val):
    """
    Only return a value if the value is the Delete status flag.

    @param val: The value to filter
    @returns: D or None
    """
    return cfg.ASMT_STATUS_DELETED if val == cfg.ASMT_STATUS_DELETED else None


def filter_twenty_characters(val):
    """
    Reduce a string value to a maximum of 20 characters.

    @param val: The value to filter
    @returns: The value trimmed to 20 characters
    """
    if val is None:
        return None
    return val[0:20] if len(val) > 20 else val


def filter_zero_padded_grade(val):
    """
    Zero-pad a grade value so that it is always a two digit string.

    @param val: The value to pad
    @returns: The value as a two-digit string
    """
    if val is None:
        return '00'
    return '%02d' % val


ALL_FILTERS = {
    'yesno': filter_yesno,
    'yesnoblank': filter_yesnoblank,
    'always_true': filter_always_true,
    'only_delete': filter_only_delete,
    'trim_to_20': filter_twenty_characters,
    'zero_pad_grade': filter_zero_padded_grade
}
