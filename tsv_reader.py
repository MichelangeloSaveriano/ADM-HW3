import os

def read_tsv(path, parse_list = False):
    try:
        with open(path, encoding="utf8") as f:
            res = dict()
            keys = f.readline().strip().split('\t')
            values = f.read().strip().split('\t')
            for k, v in zip(keys, values):
                res[k] = v
            if parse_list:
                res['bookAuthors'] = res['bookAuthors'].split(' ; ')
                res['characters'] = res['bookAuthors'].split(' ; ')
                res['setting'] = res['bookAuthors'].split(' ; ')
            return res
    except IOError:
        return None
