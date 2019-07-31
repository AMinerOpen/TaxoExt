import json

class nsfc:
    @staticmethod
    def load_discipline():
        dic = {}
        with open('data/nsfc.jl', 'r', encoding='utf-8') as f:
            for line in f:
                th = json.loads(line)
                dic[th['_id']] = th
        return dic
    discipline = load_discipline.__func__()
