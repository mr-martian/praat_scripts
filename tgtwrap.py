#!/usr/bin/env python3

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
