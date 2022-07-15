from itertools import chain
from utils import split_pinyin_str

with open('source/普通話詞語表（表一）.txt') as f1, \
        open('source/普通話詞語表（表二）.txt') as f2, \
        open('words.txt', 'w') as f3:
    for line in chain(f1, f2):
        word, pinyin_str = line.rstrip('\n').split('\t')
        word = word.lstrip('*')
        # pinyin_str = split_pinyin_str(pinyin_str)
        # print(word, pinyin_str)
        print(word, file=f3)
