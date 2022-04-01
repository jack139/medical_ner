import os
import json

categories = set()

cate_map = {
    "Medical_Examination" : "检验和检查",
    "Symptom"             : "症状和体征",
    "Operation"           : "治疗和手术",
    "Drug"                : "药物",
    "Drug_Category"       : "药物",
}

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

                    etype = cate_map[etype]

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
    convert('data/IMCS-NER/new_split/IMCS_train.json', 'dataset/imcs_train.json', False)
    convert('data/IMCS-NER/new_split/IMCS_dev.json', 'dataset/imcs_dev.json', False)

    json.dump(
        list(categories),
        open('data/imcs_categories.json', 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )
