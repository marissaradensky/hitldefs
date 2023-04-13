import json

#get ground-truth flags
flags = []
with open('../data/flags/dataSentsFlags.jsonl', 'r') as json_file:
    json_list = list(json_file)
for json_str in json_list:
    result = json.loads(json_str)
    flags.append(result["flag"])

#get feversci flags
feversciFlags = []
with open('../data/results/multivers/feversciSents.jsonl', 'r') as json_file:
    json_list = list(json_file)
for json_str in json_list:
    result = json.loads(json_str)
    if result["evidence"] == {}:
        feversciFlags.append(True)
    else:
        docid = list(result["evidence"].keys())[0]
        if result["evidence"][docid]["label"] == "CONTRADICT":
            feversciFlags.append(True)
        elif result["evidence"][docid]["sentences"] == []:
            feversciFlags.append(False)
        else:
            feversciFlags.append(False)

#get fever flags
feverFlags = []
with open('../data/results/multivers/feverSents.jsonl', 'r') as json_file:
    json_list = list(json_file)
for json_str in json_list:
    result = json.loads(json_str)
    if result["evidence"] == {}:
        feverFlags.append(True)
    else:
        docid = list(result["evidence"].keys())[0]
        if result["evidence"][docid]["label"] == "CONTRADICT":
            feverFlags.append(True)
        elif result["evidence"][docid]["sentences"] == []:
            feverFlags.append(False)
        else:
            feverFlags.append(False)

#get wanli w/ combo facts from fever flags
feverWanliBefore = ['flag', 'entailment', 'entailment', 'entailment', 'flag', 'entailment', 'flag']+['entailment', 'flag', 'entailment', 'flag', 'entailment', 'flag', 'flag', 'entailment', 'flag', 'entailment']+['entailment', 'entailment', 'flag', 'entailment', 'entailment', 'entailment', 'entailment']+['entailment', 'flag', 'entailment', 'entailment', 'flag', 'flag', 'entailment']+['flag', 'entailment', 'flag', 'entailment', 'flag', 'flag', 'flag', 'flag', 'flag', 'flag']+['entailment', 'entailment', 'entailment', 'entailment', 'entailment', 'flag']+['flag', 'entailment', 'entailment', 'entailment', 'flag', 'entailment', 'entailment']+['entailment', 'flag', 'entailment', 'entailment', 'entailment', 'entailment', 'entailment', 'entailment', 'entailment', 'flag']+['entailment', 'entailment', 'entailment', 'flag', 'entailment', 'entailment', 'flag', 'entailment']+['flag', 'entailment', 'flag', 'entailment', 'entailment', 'entailment', 'flag', 'flag', 'entailment']
feverWanliFlags = []
for f in feverWanliBefore:
    if f == "flag":
        feverWanliFlags.append(True)
    else:
        feverWanliFlags.append(False)

#get wanli w/ combo facts from fever_sci flags
feversciWanliBefore = ['flag', 'entailment', 'entailment', 'entailment', 'flag', 'entailment', 'flag']+['entailment', 'flag', 'entailment', 'flag', 'entailment', 'flag', 'flag', 'entailment', 'flag', 'flag']+['entailment', 'entailment', 'flag', 'entailment', 'entailment', 'entailment', 'entailment']+['entailment', 'flag', 'entailment', 'entailment', 'flag', 'flag', 'entailment']+['flag', 'entailment', 'flag', 'entailment', 'flag', 'flag', 'flag', 'flag', 'flag', 'flag']+['entailment', 'entailment', 'entailment', 'entailment', 'entailment', 'flag']+['flag', 'entailment', 'entailment', 'entailment', 'flag', 'entailment', 'entailment']+['entailment', 'flag', 'entailment', 'entailment', 'entailment', 'entailment', 'entailment', 'entailment', 'entailment', 'entailment']+['entailment', 'entailment', 'entailment', 'flag', 'entailment', 'entailment', 'flag', 'entailment']+['flag', 'entailment', 'flag', 'entailment', 'entailment', 'entailment', 'flag', 'flag', 'entailment']
feversciWanliFlags = []
for f in feversciWanliBefore:
    if f == "flag":
        feversciWanliFlags.append(True)
    else:
        feversciWanliFlags.append(False)

#get scores for flagging when multi (fever, fever_sci) or wanli w/ combo facts from multi (fever, fever_sci) says so
for x in [feverFlags,feversciFlags,feverWanliFlags,feversciWanliFlags]:
    TPs = 0
    TNs = 0
    FPs = 0
    FNs = 0
    for f in range(0,len(flags)):
        if x[f] == flags[f]:
            if flags[f] == True:
                TPs += 1
            else:
                TNs += 1
        else:
            if flags[f] == True:
                FNs += 1
            else:
                FPs += 1
    print("accuracy: ",(TPs+TNs)/len(flags))
    print("precision: ",(TPs)/(TPs+FPs))
    print("recall: ",(TPs)/(TPs+FNs))
    print("TPs: ",TPs)
    print("TNs: ",TNs)
    print("FPs: ",FPs)
    print("FNs: ",FNs)

# get scores for flagging whenever multi or wanli says so
for x in [[feverFlags,feverWanliFlags],[feversciFlags,feversciWanliFlags]]:
    TPs = 0
    TNs = 0
    FPs = 0
    FNs = 0
    for f in range(0,len(flags)):
        if x[0][f] == True or x[1][f] == True:
            if flags[f] == True:
                feverWTPs2 += 1
            else:
                feverWFPs2 += 1
        else:
            if flags[f] == False:
                feverWTNs2 += 1
            else:
                feverWFNs2 += 1
    print("accuracy: ",(TPs+TNs)/len(flags))
    print("precision: ",(TPs)/(TPs+FPs))
    print("recall: ",(TPs)/(TPs+FNs))
    print("TPs: ",TPs)
    print("TNs: ",TNs)
    print("FPs: ",FPs)
    print("FNs: ",FNs)
