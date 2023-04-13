import openai
import os
import re
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification
import nltk
nltk.download('punkt')
openai.api_key = #openai key here

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

# Get combo facts from Multivers. (currently manually extracted)
combineFactsFeverSci = {"shap": [[3,7]],"xgboost": [[6,7]]}
combineFactsFever = {"xgboost": [[6,7]],"bart": [[1,2],[2,4]],"roberta": [[0,1]],"skip-gram model": [[0,1]]}
combineFacts = combineFactsFeverSci

# Get Wanli entailment results.
for term in defs.keys():
    print("term: ",term)
    model = RobertaForSequenceClassification.from_pretrained('alisawuffles/roberta-large-wanli')
    tokenizer = RobertaTokenizer.from_pretrained('alisawuffles/roberta-large-wanli')
    factsFinal = facts
    # Add combo facts from Multivers, if any.
    if term in combineFacts.keys():
        for c in combineFacts[term]:
            factsFinal.append(factsFinal[c[0]]+" "+factsFinal[c[1]])

    predictions = {}
    for k in sents:
        for f in factsFinal:
            x = tokenizer(f, k, return_tensors='pt', max_length=128, truncation=True)
            logits = model(**x).logits
            probs = logits.softmax(dim=1).squeeze(0)
            label_id = torch.argmax(probs).item()
            prediction = model.config.id2label[label_id]
            if prediction == "entailment":
                predictions[k] = "entailment"
            elif k not in predictions.keys():
                predictions[k] = "flag"
    preds = []
    for p in predictions.keys():
        preds.append(predictions[p])
    print(preds)
