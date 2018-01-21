import json

with open('../pats.txt') as f:
    pats = f.readlines()
    pats_dict = {}
    for pat_str in pats:
        pat_spl = pat_str.split('|')
        pats_dict[pat_spl[0]] = float(pat_spl[1].replace('\n', ''))
    
    with open('../pats.json', 'w') as out:
        json.dump(pats_dict, out, indent=4)
