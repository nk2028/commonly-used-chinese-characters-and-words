from collections import defaultdict
import re
from typing import List
import unicodedata
import os
import itertools
import json

here = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(here, 'correct_pinyin_list.txt')) as f:
    correct_pinyin_list = [line.rstrip('\n') for line in f]

def diacritic2number(s: str) -> str:
    '''
    >>> diacritic2number('hǎo')
    'hao3'
    >>> diacritic2number('zi')
    'zi5'
    '''
    s = unicodedata.normalize('NFD', s)
    for tone, symbol in enumerate('\u0304\u0301\u030c\u0300', 1):
        if symbol in s:
            s = s.replace(symbol, '') + str(tone)
            return unicodedata.normalize('NFC', s)  # ê, ü
    return unicodedata.normalize('NFC', s + '5')

def is_valid_pinyin(s: str) -> bool:
    return s[:-1] in correct_pinyin_list and s[-1] in '12345'

# https://ayaka.shn.hk/hanregex/
han_regex = re.compile(r'[\u3006\u3007\u4e00-\u9fff\u3400-\u4dbf\U00020000-\U0002a6df\U0002a700-\U0002ebef\U00030000-\U0003134f]')
is_han = lambda c: bool(han_regex.fullmatch(c))

def determine_longest_match(i: str, x: List[str]) -> str:
    '''
    >>> determine_longest_match('123', ['1', '12'])
    '12'
    >>> determine_longest_match('12', ['1', '13'])
    '1'
    >>> determine_longest_match('a', ['1', '13'])
    ''
    '''
    max_len = 0
    for a in x:
        current_len = len(a)
        if current_len > max_len and i.startswith(a):
            max_len = current_len
    return i[:max_len]

def split_pinyin_str(s: str) -> List[str]:
    '''
    >>> split_pinyin_str('jiātíng')
    ['jia1', 'ting2']
    >>> split_pinyin_str('jiā·huo')
    ['jia1', 'huo5']
    >>> split_pinyin_str('Àoyùnhuì')
    ['ao4', 'yun4', 'hui4']
    >>> split_pinyin_str('ê̌')
    ['ê3']
    '''
    original_s = s

    if '·' in s:
        return list(itertools.chain.from_iterable(map(split_pinyin_str, s.split('·'))))  # recursion

    # remove tone symbols first
    s = unicodedata.normalize('NFD', s)
    for symbol in '\u0304\u0301\u030c\u0300':
        s = s.replace(symbol, '')
    s = unicodedata.normalize('NFC', s)

    s = s.lower()

    pinyin_list = []
    while s:
        pinyin = determine_longest_match(s, correct_pinyin_list)
        length = len(pinyin)
        if length == 0:
            raise ValueError('Unexpected pinyin string: ' + original_s)
        pinyin_list.append(pinyin)
        s = s[length:]

    s = original_s
    s = unicodedata.normalize('NFD', s)

    pinyin_with_tone_list = []
    for pinyin in pinyin_list:
        pinyin = unicodedata.normalize('NFD', pinyin)
        length = len(pinyin)
        length += 1  # add tone
        pinyin_with_tone = s[:length]
        pinyin_with_tone = pinyin_with_tone.lower()
        pinyin_with_tone = unicodedata.normalize('NFC', pinyin_with_tone)
        pinyin_with_tone = diacritic2number(pinyin_with_tone)
        assert is_valid_pinyin(pinyin_with_tone), original_s
        pinyin_with_tone_list.append(pinyin_with_tone)
        s = s[length:]

    return pinyin_with_tone_list
