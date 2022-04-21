#!/usr/bin/env python3

import tgt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('infile', action='store')
parser.add_argument('word_tier', action='store')
parser.add_argument('phon_tier', action='store')
args = parser.parse_args()

tg = None
for enc in ['utf-8', 'utf-16']:
    try:
        tg = tgt.io.read_textgrid(args.infile, encoding=enc)
        break
    except:
        pass

labels = ['word', 'pre-vowel', 'click', 'post-vowel',
          'pre-nasal len', 'pre-silence len', 'pre-vowel len',
          'click len', 'aspiration len', 'post-vowel len']

print('\t'.join(labels))

w_tier = tg.get_tiers_by_name(args.word_tier)[0]
p_tier = tg.get_tiers_by_name(args.phon_tier)[0]
for an in w_tier.annotations:
    word = an.text
    start = an.start_time
    end = an.end_time
    pieces = []
    for sub_an in p_tier.annotations:
        if sub_an.start_time >= start and sub_an.end_time <= end:
            pieces.append((sub_an.text, sub_an.start_time,
                           round((sub_an.end_time - sub_an.start_time)*1000)))
    if len(pieces) < 2:
        continue
    pieces.sort(key=lambda x: x[1])
    prev = ('', 0, 0)
    pren = ('', 0, 0)
    pres = ('', 0, 0)
    asp = ('', 0, 0)
    postv = pieces.pop()
    if pieces[-1][0] == 'ʰ':
        asp = pieces.pop()
    click = pieces.pop()
    for p in pieces:
        if p[0] == 'n':
            pren = p
        elif p[0] == '-':
            pres = p
        else:
            prev = p
    ls = [str(p[2]) for p in [pren, pres, prev, click, asp, postv]]
    print(f'{word}\t{prev[0]}\t{click[0]}\t{postv[0]}\t' + '\t'.join(ls))
