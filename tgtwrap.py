#!/usr/bin/env python3

import parselmouth
import tgt

def load(fname):
    for enc in ['utf-8', 'utf-16']:
        try:
            return tgt.io.read_textgrid(fname, encoding=enc)
        except:
            pass
    return None

def skip_empty(tier, skipx=True):
    for an in tier.annotations:
        if not an.text.strip():
            continue
        elif skipx and an.text.strip() == 'XXX':
            continue
        yield an

def get_contains(tier, an, skipblank=True, skipx=True,
                 fillempty=False, matchtime=False):
    ls = tier.get_annotations_between_timepoints(an.start_time, an.end_time)
    got_any = False
    for sub_an in ls:
        if skipblank and not sub_an.text.strip():
            continue
        elif skipx and sub_an.text.strip() == 'XXX':
            continue
        yield sub_an
        got_any = True
    if not got_any and fillempty:
        if matchtime:
            yield tgt.Annotation(an.start_time, an.end_time, 'XXX')
        else:
            yield tgt.Annotation(0, 0, 'XXX')

def all_contains(tg, an, **kwargs):
    ret = {}
    for t in tg.tiers:
        ret[t.name] = list(get_contains(t, an, **kwargs))
    return ret

def annotation_tree(tg, tier, skipx=True, **kwargs):
    return [all_contains(tg, an, skipx=skipx, **kwargs)
            for an in skip_empty(tier, skipx=skipx)]

def add_formant_args(parser):
    parser.add_argument('--max-formant', '-f', type=float, default=5000.0)
    parser.add_argument('--formant-count', '-c', type=float, default=5.0)
    parser.add_argument('--window-length', '-w', type=float, default=0.025)

def formants_from_args(sound, args):
    return sound.to_formant_burg(
        max_number_of_formants = args.formant_count,
        maximum_formant = args.max_formant,
        window_length = args.window_length
    )

def add_file_args(parser, formants=True, default_tier='word'):
    parser.add_argument('sound', action='store')
    parser.add_argument('textgrid', action='store')
    parser.add_argument('--tier', '-t', default=default_tier)
    if formants:
        add_formant_args(parser)

def data_from_args(args, formants=True):
    sound = parselmouth.Sound(args.sound)
    tg = load(args.textgrid)
    tier = tg.get_tiers_by_name(args.tier)[0]
    if formants:
        return sound, tg, tier, formants_from_args(sound, args)
    else:
        return sound, tg, tier
