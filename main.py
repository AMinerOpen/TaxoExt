from src.config import config
import json
import math
from collections import defaultdict
from collections import Counter

global_freq = Counter()
global_score = defaultdict(float)

print('calculating word scores...')

cnt = 0
with open('data/nsfc_kws_filt.jl', 'r', encoding='utf-8') as f:
    for line in f:
        cnt += 1
        if cnt % 10 == 0:
            print(cnt, end='\r')
            # break
        th = json.loads(line)
        for x in th['words']:
            global_freq[x[0]] += 1
            global_score[x[0]] += x[1]
for k in global_score:
    global_score[k] /= global_freq[k]
print(cnt, 'documents calculated over.')

print('extending taxonomy...')

words = set()

id2code = {}

with open('data/nsfc_ids.jl', 'r', encoding='utf-8') as f:
    for line in f:
        th = json.loads(line)
        id2code[th['_id']] = th['sid']

from src.nsfc import nsfc

from collections import Counter
from collections import defaultdict

wdcoo = defaultdict(Counter)
docc = Counter()

cnt = 0
with open('data/nsfc_kws_filt.jl', 'r', encoding='utf-8') as f:
    for line in f:
        cnt += 1
        if cnt % 10 == 0:
            print(cnt, end='\r')
            # break
        th = json.loads(line)
        if th['_id'] not in id2code: continue
        code = id2code[th['_id']]
        if code not in nsfc.discipline or not nsfc.discipline[code]['is_leaf']: continue
        new_words = []
        for x in th['words']:
            if global_score[x[0]] >= config.MIN_SCORE and global_freq[x[0]] >= config.MIN_FREQ:
                new_words.append(x)
                words.add(x[0])
        docc[code] += 1
        for x in new_words:
            wdcoo[x[0]][code] += x[1]

print(cnt, 'documents over.')

print('vocab:', len(words), 'words.')

wd = defaultdict(lambda: defaultdict(float))
total = sum(docc.values())

g = open('data/result.jl', 'w', encoding='utf-8')

cnt = 0
for w in wdcoo:
    cnt += 1
    if cnt % 100 == 0:
        print(cnt, end='\r')
    d_tot = sum(wdcoo[w].values())
    for d in wdcoo[w]:
        wd[w][d] = wdcoo[w][d] * total / d_tot / docc[d]
    norm = sum(wd[w].values())
    for d in wd[w]:
        wd[w][d] /= norm
    th = {}
    th['word'] = w
    th['parents'] = [(x[0], round(x[1], 3)) for x in sorted(wd[w].items(), key=lambda x:x[1], reverse=True) if x[1] >= config.MIN_PROB]
    g.write(json.dumps(th, ensure_ascii=False))
    g.write('\n')

g.close()
print(cnt, 'words saved in data/result.jl.')
