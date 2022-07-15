from utils import diacritic2number, is_han, is_valid_pinyin
from itertools import chain

s = set()

with open('source/常用字表.txt') as f:
    for i, line in enumerate(f, 1):
        pinyin, chars = line.rstrip('\n').split('\t')
        pinyin = diacritic2number(pinyin)
        assert is_valid_pinyin(pinyin), (i, pinyin)
        for ch in chars:
            if ch in '▲()':
                continue
            s.add(ch)

with open('source/普通話詞語表（表一）.txt') as f1, \
        open('source/普通話詞語表（表二）.txt') as f2:
    for line in chain(f1, f2):
        word, pinyin_str = line.rstrip('\n').split('\t')
        word = word.lstrip('*')
        s.add(word)

l = sorted(s, key=lambda x: (len(x), x))

with open('all.txt', 'w') as f:
    for word in l:
        print(word, file=f)
