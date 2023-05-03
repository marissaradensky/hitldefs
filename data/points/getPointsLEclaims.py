import csv
import json
import pickle
import string
import spacy
import subprocess

# START - FROM LONGEVAL WORK
try:
    nlp = spacy.load('en_core_web_lg')
    # nlp.add_pipe('sentencizer', before="parser")
except OSError:
    raise OSError("'en_core_web_lg model' is required unless loading from cached file."
                    "To install: 'python -m spacy download en_core_web_lg'")

def get_sents(text, return_nlp=False):
    if not isinstance(text, str):
        # assume it is list or tuple of strings
        return text
    global nlp
    nlp_sents = [x for x in nlp(text).sents]
    if return_nlp:
        return nlp_sents
    else:
        return [x.text for x in nlp_sents]

def split_sents(text, length_threshold=5):
    """Break up sentences into clauses and phrases."""
    sents = get_sents(text, return_nlp=True)
    all_sent_units = []
    for s1 in sents:
        if not s1.text.strip():
            continue
        pos_tags = [x.pos_ for x in s1]
        tokens = [x.text for x in s1]
        all_units = []
        for i, (pt, tk) in enumerate(zip(pos_tags, tokens)):
            if tk in [',', '!', '?', ';'] or 'CONJ' in pt:
                if tk == "that":
                    continue
                all_units.append(i)

        all_units.append(len(s1))


        # combine short units together
        combined_units = []
        for i in range(0, len(all_units)):
            if i == 0 or (all_units[i] - all_units[i - 1]) > length_threshold:
                combined_units.append(all_units[i])
            else:
                combined_units[-1] = all_units[i]

        if combined_units[0] <= length_threshold:
            combined_units = combined_units[1:]

        unit_strs = []
        for i in range(len(combined_units)):
            if i == 0:
                unit_strs.append(s1[0:combined_units[i]].text)
            else:
                unit_strs.append(s1[combined_units[i - 1] + 1:combined_units[i]].text)
        all_sent_units.append(unit_strs)

    return all_sent_units, [x.text for x in sents]
# END - FROM LONGEVAL WORK

# Get definitions.
defs = None
with open("defs.txt") as fi:
    defs = fi.read()
defs = json.loads(defs)

# Get claims.
claims = {}
cs = []
for t in defs.keys():
    out = split_sents(defs[t])[0]
    for x in out:
        cs += x
    claims[t] = cs
    cs = []

# Write claims to file.
f = open("pointsLEclaims.txt", "a")
f.write(str(claims))
f.close()
