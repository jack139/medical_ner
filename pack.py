import os
import glob
import json

def pack_file(file_list, outfile):
    D = []
    for f in file_list:
        data = json.load(open(f))
        D.extend(data)

    json.dump(
        D,
        open(outfile, 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )

    print(len(D))

if __name__ == '__main__':
    pack_file(glob.glob('dataset/*train.json'), 'data/pack_train.json')
    pack_file(glob.glob('dataset/*dev.json'), 'data/pack_dev.json')
