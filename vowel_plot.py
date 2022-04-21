#!/usr/bin/env python3

import matplotlib.pyplot as plt
import parselmouth # pip3 install praat-parselmouth
import tgt # pip3 install tgt

def plot_vowels(sndfname, tgfname, plotfname,
                tiername='vowel',
                max_number_of_formants=5.0, maximum_formant=5500.0,
                window_length=0.025):
    snd = parselmouth.Sound(sndfname)
    formants = snd.to_formant_burg(
        max_number_of_formants = max_number_of_formants,
        maximum_formant = maximum_formant,
        window_length = window_length
    )
    tg = tgt.io.read_textgrid(tgfname, encoding='utf-16')
    tier = tg.get_tiers_by_name(tiername)[0]
    f1 = []
    f2 = []
    lab = []
    for an in tier.annotations:
        lab.append(' '+an.text+' ')
        t = (an.start_time + an.end_time) / 2
        f1.append(formants.get_value_at_time(1, t))
        f2.append(formants.get_value_at_time(2, t))
    fig, ax = plt.subplots()
    ax.scatter(f2, f1, marker=None, s=0)
    ax.set_clip_on(False)
    for i in range(len(lab)):
        ax.text(f2[i], f1[i], lab[i], ha='center', va='center')
    ax.invert_xaxis()
    ax.invert_yaxis()
    ax.set_xlabel('F2 (Hz)')
    ax.set_ylabel('F1 (Hz)')
    plt.savefig(plotfname)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('sound', action='store')
    parser.add_argument('textgrid', action='store')
    parser.add_argument('plot', action='store')
    parser.add_argument('--tier', '-t', default='vowel')
    parser.add_argument('--max-formant', '-f', type=float, default=5000.0)
    parser.add_argument('--formant-count', '-c', type=float, default=5.0)
    parser.add_argument('--window-length', '-w', type=float, default=0.025)
    args = parser.parse_args()
    plot_vowels(
        args.sound, args.textgrid, args.plot,
        tiername = args.tier,
        max_number_of_formants = args.formant_count,
        maximum_formant = args.max_formant,
        window_length = args.window_length
    )
