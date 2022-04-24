#!/usr/bin/env python3

import matplotlib.pyplot as plt
import parselmouth
import tgt
import tgtwrap
import os

def pull_formants(args):
    snd, tg, tier, formants = tgtwrap.data_from_args(args, formants=True)
    pref = args.label + '\t' if args.label else ''
    for block in tgtwrap.annotation_tree(tg, tier):
        for name in block:
            for an in block[name]:
                lab = an.text.strip('/').strip('[').strip(']')
                t = (an.start_time + an.end_time) / 2
                f1 = formants.get_value_at_time(1, t)
                f2 = formants.get_value_at_time(2, t)
                print(f'{pref}{name}\t{lab}\t{f1}\t{f2}')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser('Data extractor of Phonetics Arabic L2 final project')
    tgtwrap.add_file_args(parser, formants=True)
    parser.add_argument('--label', '-l', action='store', default='')
    args = parser.parse_args()
    pull_formants(args)
