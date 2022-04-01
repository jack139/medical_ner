import json

new_ratio = 0.1

categories = set()

cate_map = {
    "ite" : "检验和检查",
    "dis" : "疾病和诊断",
    "sym" : "症状和体征",
    "pro" : "治疗和手术",
    "bod" : "解剖部位",
    "dru" : "药物",
}

def get_data(infile, include_blank=True):
    D = []
    data = json.load(open(infile))

    for d in data:
        entities = []
        for e in d['entities']:
            categories.add(e['type'])

            if e['type'] in ['equ', 'mic', 'dep']:
                continue

            e['type'] = cate_map[e['type']]
            entities.append(e)

        # 加入数据集
        if include_blank or len(entities)>0:
            D.append({
                'text' : d['text'],
                'entities' : entities,
            })

    #print(len(D))
    return D


if __name__ == '__main__':

    D_train = get_data('data/CMeEE/CMeEE_train.json', False)
    D_dev = get_data('data/CMeEE/CMeEE_dev.json', False)

    # 重新分割
    train_num = len(D_train)
    dev_num = len(D_dev)

    print(f"train: {train_num}\tdev: {dev_num}")

    new_dev_num = int((train_num + dev_num) * new_ratio)

    print(f"new train: {train_num+(dev_num-new_dev_num)}\tnew dev: {new_dev_num}")

    json.dump(
        D_train + D_dev[:-new_dev_num],
        open('dataset/cmeee_train.json', 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )

    json.dump(
        D_dev[-new_dev_num:],
        open('dataset/cmeee_dev.json', 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )

    json.dump(
        list(categories),
        open('data/cmeee_categories.json', 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )
