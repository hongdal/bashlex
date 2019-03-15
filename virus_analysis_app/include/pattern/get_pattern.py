import json 

patterns = {}

with open('../../.cache/output.json') as json_file:
    data = json.load(json_file)
    for r in data:
        if r['tags'] not in patterns:
            patterns[r['tags']] = set()
        patterns[r['tags']].add(r['id'])
    
for k, v in patterns.items():
    if k != 'None':
        print("%s: %d" % (k, len(v)))
        print(v)        
