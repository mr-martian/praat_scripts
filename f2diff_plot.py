#!/usr/bin/env python3

import matplotlib.pyplot as plt
import argparse
import itertools

parser = argparse.ArgumentParser('plot data from Phonetics L2 Arabic final project')
parser.add_argument('--speaker', '-s', action='store', default='')
parser.add_argument('tsv', action='store')
args = parser.parse_args()

diacritics = ['ˤ', 'ʶ']
cons = ['consonant', 'onset']
colors = {
    'a': 'red',
    'aː': 'lime',
    'aʶ': 'darkred',
    'i': 'blue',
    'iʶ': 'darkblue',

    'd̪': 'tan',
    'dˤ': 'orange',
    'θ': 'red',
    'ðˤ': 'darkred',
    's': 'lime',
    'sˤ': 'darkgreen',
    't̪': 'blue',
    'tˤ': 'darkblue',
}
cv_split = [['t̪', 'tˤ', 'd̪', 'dˤ', 's', 'sˤ', 'θ', 'ðˤ'],
            ['a', 'aː', 'aʶ', 'i', 'iʶ']]
phon_split = [['t̪', 'tˤ'], ['d̪', 'dˤ'], ['s', 'sˤ'], ['θ', 'ðˤ'],
              ['a', 'aʶ'], ['i', 'iʶ']]

def make_subplot(ax, data):
    data.sort(key=lambda x: x[0])
    fsums = [0, 0, 0, 0]
    fcts = [0, 0]
    for k, g in itertools.groupby(data, lambda x: x[0]):
        lab = ' '+k+' '
        color = colors.get(k, 'grey')
        gp = list(g)
        f1 = [x[1] for x in gp]
        f2 = [x[2] for x in gp]
        af1 = sum(f1) / len(f1)
        af2 = sum(f2) / len(f2)
        ax.scatter(f2, f1, s=1, color=color, label=k)
        ax.text(af2, af1, lab, ha='center', va='center', color=color)
        if k[-1] in diacritics:
            fsums[2] += sum(f1)
            fsums[3] += sum(f2)
            fcts[1] += len(f1)
        else:
            fsums[0] += sum(f1)
            fsums[1] += sum(f2)
            fcts[0] += len(f1)
    fsums[0] /= fcts[0]
    fsums[1] /= fcts[0]
    fsums[2] /= fcts[1]
    fsums[3] /= fcts[1]
    ax.arrow(fsums[1], fsums[0], fsums[3]-fsums[1], fsums[2]-fsums[0],
             head_width=20, length_includes_head=True, zorder=-5)
    ax.set_clip_on(False)
    ax.set_xlabel('F2 (Hz)')
    ax.set_ylabel('F1 (Hz)')

data = [[], []]
with open(args.tsv) as fin:
    first = True
    for line in fin:
        if first:
            first = False
            continue
        name, lang, tier, text, f1, f2 = line.strip().split('\t')
        h = 0 if lang == 'Arabic' else 1
        if args.speaker:
            if args.speaker == name:
                h = 0
            else:
                continue
        data[h].append((text, float(f1), float(f2)))

def filter_and_plot(ax, data, pattern, legend):
    make_subplot(ax, [d for d in data if d[0] in pattern])
    if legend:
        ax.legend(bbox_to_anchor=(1.0,0.5), loc='center left')

def make_fig(data, pattern, fname):
    fig, axs = plt.subplots(2, 2, sharex=True, sharey='row', figsize=(8.4, 4.8))
    axs[0,0].set_title('Arabic L1')
    axs[0,1].set_title('English L1')
    for h in range(2):
        for v, s in enumerate(pattern):
            filter_and_plot(axs[v,h], data[h], s, h == 1)
    axs[0,0].invert_xaxis()
    axs[0,0].invert_yaxis()
    axs[1,1].invert_yaxis()
    for ax in fig.get_axes():
        ax.label_outer()

    plt.savefig(fname)

def make_fig_single(data, fname):
    fig, axs = plt.subplots(4, sharex=True, sharey=True, figsize=(4.4,9))
    filter_and_plot(axs[0], data, cv_split[0]+cv_split[1], True)
    axs[0].set_title('All Segments')
    filter_and_plot(axs[1], data, phon_split[0]+phon_split[1], True)
    axs[1].set_title('Stops')
    filter_and_plot(axs[2], data, phon_split[2]+phon_split[3], True)
    axs[2].set_title('Fricatives')
    filter_and_plot(axs[3], data, phon_split[4]+phon_split[5], True)
    axs[3].set_title('Vowels')
    axs[0].invert_xaxis()
    axs[0].invert_yaxis()
    for ax in fig.get_axes():
        ax.label_outer()
    plt.tight_layout()
    plt.savefig(fname)

if args.speaker:
    make_fig_single(data[0], args.speaker + '.png')
else:
    make_fig(data, cv_split, 'data-all.png')
    make_fig(data, phon_split[:2], 'data-stop.png')
    make_fig(data, phon_split[2:4], 'data-fricative.png')
    make_fig(data, phon_split[4:], 'data-vowel.png')
