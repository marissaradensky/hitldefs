import json

#get ground-truth flags
flags = []
with open('../data/flags/dataFlags.jsonl', 'r') as json_file:
    json_list = list(json_file)
for json_str in json_list:
    result = json.loads(json_str)
    flags.append(result["flag"])

#get feversci flags
feversciFlags = []
with open('../data/results/multivers/feversciClaims.jsonl', 'r') as json_file:
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
with open('../data/results/multivers/feverClaims.jsonl', 'r') as json_file:
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

#get scores for flagging when multi (fever, fever_sci) says so
for x in [feverFlags,feversciFlags]:
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
