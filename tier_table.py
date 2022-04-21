#!/usr/bin/python3

import tgt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('infile', action='store')
parser.add_argument('word_tier', action='store')
parser.add_argument('--label', nargs='+', default=[])
args = parser.parse_args()

tg = None
for enc in ['utf-8', 'utf-16']:
    try:
        tg = tgt.io.read_textgrid(args.infile, encoding=enc)
        break
    except:
        pass

names = sorted(n for n in tg.get_tier_names() if n != args.word_tier)
tiers = [tg.get_tiers_by_name(n)[0] for n in names]

print(args.word_tier, end='\t')
for n in names:
    print(n, end='\t')
    if n in args.label:
        print(n + ' label', end='\t')
print('')

w_tier = tg.get_tiers_by_name(args.word_tier)[0]
for an in w_tier.annotations:
    print(an.text, end='\t')
    start = an.start_time
    end = an.end_time
    for n, t in zip(names, tiers):
        for sub_an in t.annotations:
            if sub_an.text == 'XXX':
                continue
            if sub_an.start_time >= start and sub_an.end_time <= end:
                print(sub_an.end_time - sub_an.start_time, end='\t')
                if n in args.label:
                    print(sub_an.text, end='\t')
                break
        else:
            print('0', end='\t')
            if n in args.label:
                print('XXX', end='\t')
    print('')
