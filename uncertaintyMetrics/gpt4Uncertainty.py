import openai
import os
import re
import json
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification
import nltk
nltk.download('punkt')
openai.api_key = #openai api key here

factsFile = "../data/facts/factsOrigSents.txt"
pointsFile = "../data/points/pointsLEsents.txt"

# Get facts. Facts are semantic units from primary sources related to each term defined. May be sentences, clauses, claims, etc.
facts = None
with open(factsFile) as fi:
    facts = fi.read()
facts = json.loads(facts)

# Get points. Points are semantic units from definitions. May be sentences, clauses, claims, etc.
points = None
with open(pointsFile) as fi:
    points = fi.read()
points = json.loads(points)

# Get prompt for producing GPT-4 uncertainty verdict for a claim and its related facts.
def generate_verdict(point,facts):
    return """{1}\n\nIs the claim below fully, partially, or not entailed by the texts above? Explain your reasoning step by step and then answer the question. Claim: {0}""".format(point,facts)

# Get GPT-4 uncertainty responses for each term's claims based on term-related facts.
terms = facts.keys()
for term in terms:
    print("term: ",term)
    f = facts[term]
    for p in points[term]:
        print("claim: ",p)
        print("prompt: ",generate_verdict(p,f))
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": generate_verdict(p,f)}
            ],
            temperature=0,
            max_tokens=500,
        )
        print(response)
