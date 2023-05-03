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
# END - FROM LONGEVAL WORK

# Get definitions.
defs = None
with open("defs.txt") as fi:
    defs = fi.read()
defs = json.loads(defs)

# Get sentences.
sents = {}
for t in defs.keys():
    sents[t] = get_sents(defs[t])

# Write sentences to file.
f = open("pointsLEsents.txt", "a")
f.write(str(sents))
f.close()
