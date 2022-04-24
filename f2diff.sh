#!/bin/bash

printf 'Speaker\tL1\tTier\tToken\tF1\tF2\n'
py=`dirname "$0"`"/f2diff.py"
for tg in *.TextGrid
do
    snd="${tg/TextGrid/wav}"
    if [[ -f "$snd" ]]; then
        pref1="${tg/.TextGrid/}"
        pref2=${pref1/_L1/$'\t'}
        python3 "$py" "$snd" "$tg" -l "$pref2" -t word 2>/dev/null || \
            python3 "$py" "$snd" "$tg" -l "$pref2" -t Word
    fi
done | grep -iE "consonant|vowel|onset|nucleus"
