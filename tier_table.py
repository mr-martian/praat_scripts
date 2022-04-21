#!/usr/bin/env python3

import tgt
import tgtwrap
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('infile', action='store')
parser.add_argument('word_tier', action='store')
parser.add_argument('--label', nargs='+', default=[])
args = parser.parse_args()

tg = tgtwrap.load(args.infile)

names = sorted(n for n in tg.get_tier_names() if n != args.word_tier)
w_tier = tg.get_tiers_by_name(args.word_tier)[0]
data = [tgtwrap.all_contains(tg, an, fillempty=True) for an in tgtwrap.skip_empty(w_tier)]

print(args.word_tier, end='\t')
for n in names:
    print(n, end='\t')
    if n in args.label:
        print(n + ' label', end='\t')
print('')

for blob in data:
    print(blob[args.word_tier][0].text, end='\t')
    for n in names:
        print(blob[n][0].duration(), end='\t')
        if n in args.label:
            print(blob[n][0].text, end='\t')
    print('')
