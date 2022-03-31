import os
import json

'''
  {
    "text": "对儿童SARST细胞亚群的研究表明，与成人SARS相比，儿童细胞下降不明显，证明上述推测成立。",
    "entities": [
      {
        "start_idx": 3,
        "end_idx": 9,
        "type": "bod",
        "entity": "SARST细胞"
      },
      {
        "start_idx": 19,
        "end_idx": 24,
        "type": "dis",
        "entity": "成人SARS"
      }
    ]
  },

'''
categories = set()

def convert(infile, outfile, include_blank=True):

    D = []
    text = ''
    entities = []
    all_idx = 0
    start_idx = 0
    etype = ''

    data = json.load(open(infile))

    for k in data.keys():
        for diag in data[k]['dialogue']:
            text = diag['sentence']

            for label in diag['BIO_label'].split():
                if label[0]=='O':
                    if etype!='':
                        entities.append({
                            "start_idx": start_idx,
                            "end_idx": all_idx - 1,
                            "type": etype,
                            "entity": text[start_idx:all_idx],
                        })
                    start_idx = 0
                    etype = ''
                elif label[0]=='B':
                    if etype!='':
                        entities.append({
                            "start_idx": start_idx,
                            "end_idx": all_idx - 1,
                            "type": etype,
                            "entity": text[start_idx:all_idx],
                        })                
                    start_idx = all_idx
                    etype = label.split('-')[1]

                    categories.add(etype)

                elif label[0]=='I':
                    pass
                else:
                    print('unknown label: ', label)

                all_idx += 1


            # 一行text结束
            if etype!='':
                entities.append({
                    "start_idx": start_idx,
                    "end_idx": all_idx - 1,
                    "type": etype,
                    "entity": text[start_idx:all_idx],
                })

            # 加入数据集
            if include_blank or len(entities)>0:
                D.append({
                    'text' : text,
                    'entities' : entities,
                })

            text = ''
            entities = []
            all_idx = 0
            start_idx = 0
            etype = ''

    json.dump(
        D,
        open(outfile, 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )

    print(len(D))


if __name__ == '__main__':
    convert('data/IMCS-NER/new_split/IMCS_train.json', 'data/imcs_train.json', False)
    convert('data/IMCS-NER/new_split/IMCS_dev.json', 'data/imcs_dev.json', False)

    json.dump(
        list(categories),
        open('data/imcs_categories.json', 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )
