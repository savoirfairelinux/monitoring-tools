# -*- coding: utf-8 -*-

"""
Helpers to parse a byte amount.
"""

import re

#############################################################################

class PercentValue(object):
    ''' Represents a % quantity
    '''
    def __repr__(self):
        return '%s%%' % self

class IntPercentValue(PercentValue, int):
    pass

class FloatPercentValue(PercentValue, float):
    pass

#############################################################################

class ByteAmountParser(object):

    # a (positive (or null) only) number,
    # optionally with decimal after a dot or a comma:
    _amount_reg = '(?P<amount>\d+(?:[.,]\d+)?)'

    def __init__(self, name, unit_transformers):
        '''
        :param name: The name of the parser.
        :param unit_transformers: a dict with as key a unit, and as value its multiplier value.
        :return: The parser.
        '''
        self.name = name
        self.unit_transformers = unit_transformers
        self.regstr = self._amount_reg + _make_reg_unit(unit_transformers)
        self.regex = re.compile(self.regstr)

    def __call__(self, value):
        match = self.regex.match(value)
        if not match:
            raise ValueError('%r is an invalid value for a %s amount ; must match following regex: %r' % (
                             value, self.name, self.regstr))
        amount = match.group(1).replace(',', '.')
        type_ = float if '.' in amount else int
        amount = type_(amount)
        transformer = self.unit_transformers[match.group(2)]
        return transformer(amount)

#############################################################################

def reg_sorted(values):
    # For use for dynamic regex construction (see below):
    # we have to sort by length (desc) so that the longer possible value
    # will be matched first:
    return sorted(values, key=lambda s: (-len(s), s))

#############################################################################

def _make_reg_unit(values):
    return '(?P<unit>%s)' % '|'.join(reg_sorted(values))

#############################################################################
###

def best_num_type(value):
    ''' Make sure to get 2 instead of 2.0 ..
    :param value:
    :return:
    '''
    int_value = int(value)
    return value if int_value != value else int_value

unit_to_transformer = {
    'TB': lambda value: best_num_type(value * 2**40),
    'GB': lambda value: best_num_type(value * 2**30),
    'MB': lambda value: best_num_type(value * 2**20),
    'KB': lambda value: best_num_type(value * 2**10),
}

byte_amount_parser = ByteAmountParser('byte', unit_to_transformer)

def make_byte_amount(value):
    ''' Parse a "computer size" value: <amount><unit>

    The supplied value can so have a unit like TB, GB, MB or KB.

    :return: The parsed value in number of bytes.

    >>> make_byte_amount('1.5GB')
    1610612736

    >>> make_byte_amount('33MB')
    34603008

    >>> make_byte_amount('1.7GB')
    1825361100.8

    >>> make_byte_amount('25%')
    Traceback (most recent call last):
      ...
    ValueError: '25%' is an invalid value for a byte amount ; must match following regex: '(?P<amount>\\\d+(?:[.,]\\\d+)?)(?P<unit>GB|KB|MB|TB)'
    '''
    return byte_amount_parser(value)


#############################################################################

adv_byte_unit_to_transformer = unit_to_transformer.copy()
adv_byte_unit_to_transformer['%'] = lambda value: { # the supplied value can only be int or float
    int: IntPercentValue,
    float: FloatPercentValue
}[type(value)](value)

byte_or_percent_amount_parser = ByteAmountParser('byte or byte-percent', adv_byte_unit_to_transformer)

def make_byte_or_pc_amount(value):
    ''' Parse a "computer size" value in string format: "<amount>(<unit>)"

     Value can so have a unit like TB, GB, MB or KB.
     It can also be '%' to represent a percentage value.
        In this case the returned value is a `PercentValue´ instance.

    :param value: The string value to be parsed.
    :return: The parsed value in number of bytes or a PercentValue instance if the '%' unit was used.

    >>> make_byte_or_pc_amount('1.5GB')
    1610612736

    >>> make_byte_or_pc_amount('33MB')
    34603008

    >>> make_byte_or_pc_amount('50%')
    50%

    >>> make_byte_or_pc_amount('15.25%')
    15.25%

    >>> make_byte_or_pc_amount('invalid')
    Traceback (most recent call last):
      ...
    ValueError: 'invalid' is an invalid value for a byte or byte-percent amount ; must match following regex: '(?P<amount>\\\d+(?:[.,]\\\d+)?)(?P<unit>GB|KB|MB|TB|%)'

    '''
    return byte_or_percent_amount_parser(value)

#############################################################################
