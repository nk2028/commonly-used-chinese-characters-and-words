from collections import defaultdict
from utils import diacritic2number, is_han, is_valid_pinyin

d = defaultdict(set)

with open('source/常用字表.txt') as f:
    for i, line in enumerate(f, 1):
        pinyin, chars = line.rstrip('\n').split('\t')
        pinyin = diacritic2number(pinyin)
        assert is_valid_pinyin(pinyin), (i, pinyin)
        for ch in chars:
            if ch in '▲()':
                continue
            assert is_han(ch), (i, ch)
            assert pinyin not in d[ch], (i, ch, pinyin)
            d[ch].add(pinyin)

with open('char.txt', 'w') as f:
    for ch, pinyins in d.items():
        # print(ch, ','.join(sorted(pinyins)), sep='\t', file=f)
        print(ch, file=f)
