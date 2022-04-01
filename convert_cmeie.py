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

new_ratio = 0.1

def search(pattern, sequence):
    """从sequence中寻找子串pattern
    如果找到，返回第一个下标；否则返回-1。
    """
    n = len(pattern)
    for i in range(len(sequence)):
        if sequence[i:i + n] == pattern:
            return i
    return -1


def get_data(infile, include_blank=True):

    D = []

    with open(infile, encoding='utf-8') as f:
        for l in f:
            l = json.loads(l)

            text = l['text']
            entities = []

            for e in l['spo_list']:
                s = e['subject']
                s_type = e['subject_type']
                o = e['object']['@value']
                o_type = e['object_type']['@value']

                s_idx = search(s, text)
                o_idx = search(o, text)

                categories.add(s_type)
                categories.add(o_type)

                if s_idx == -1 or o_idx == -1:
                    print('fail: ', s_idx, o_idx, text, e) # 未找到
                    continue

                entities.append({
                    "start_idx": s_idx,
                    "end_idx": s_idx + len(s) - 1,
                    "type": s_type,
                    "entity": s,
                })

                entities.append({
                    "start_idx": o_idx,
                    "end_idx": o_idx + len(o) - 1,
                    "type": o_type,
                    "entity": o,
                })

            # 加入数据集
            if include_blank or len(entities)>0:
                D.append({
                    'text' : text,
                    'entities' : entities,
                })


    return D


if __name__ == '__main__':

    D_train = get_data('data/CMeIE/CMeIE_train.jsonl', False)
    D_dev = get_data('data/CMeIE/CMeIE_dev.jsonl', False)

    # 重新分割
    train_num = len(D_train)
    dev_num = len(D_dev)

    print(f"train: {train_num}\tdev: {dev_num}")

    new_dev_num = int((train_num + dev_num) * new_ratio)

    print(f"new train: {train_num+(dev_num-new_dev_num)}\tnew dev: {new_dev_num}")

    json.dump(
        D_train + D_dev[:-new_dev_num],
        open('data/cmeie_train.json', 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )

    json.dump(
        D_dev[-new_dev_num:],
        open('data/cmeie_dev.json', 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )


    json.dump(
        list(categories),
        open('data/cmeie_categories.json', 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )
