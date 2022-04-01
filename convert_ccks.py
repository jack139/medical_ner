import json

new_ratio = 0.2

categories = set()

cate_map = {
    "实验室检验" : "检验和检查",
    "影像检查"   : "检验和检查",
    "疾病和诊断" : "疾病和诊断",
    "手术"      : "治疗和手术",
    "解剖部位"   : "解剖部位",
    "药物"      : "药物",
}

def get_data(infile, include_blank=True):
    D = []

    with open(infile, encoding='utf-8') as f:
        for l in f:
            l = json.loads(l)

            entities = []
            for e in l['entities']:
                categories.add(e['label_type'])

                entities.append({
                    "start_idx": e['start_pos'],
                    "end_idx": e['end_pos']-1,
                    "type": cate_map[e['label_type']],
                    "entity": l['originalText'][e['start_pos']:e['end_pos']]
                })

            if include_blank or len(entities)>0:
                if len(l['originalText'])>512:
                    # 对超长文本的处理：分成两个文本
                    for n in range(512, 0, -1):
                        if l['originalText'][n] in ['；', '，', '。', ',', '）', '、', ';']:
                            break

                    if n==0: # 连续512个字符 无分隔符，一般不可能发生
                        D.append({
                            'text' : l['originalText'],
                            'entities' : entities,
                            'too_long' : 1
                        })
                    else:
                        # 分成两个 文本
                        text1 = l['originalText'][:n]
                        text2 = l['originalText'][n:]
                        entities1 = []
                        entities2 = []

                        for ee in entities:
                            if ee['start_idx']<n:
                                entities1.append({
                                    "start_idx": ee['start_idx'],
                                    "end_idx": ee['end_idx'],
                                    "type": ee['type'],
                                    "entity": ee['entity']
                                })
                            else:
                                entities2.append({
                                    "start_idx": ee['start_idx']-n,
                                    "end_idx": ee['end_idx']-n,
                                    "type": ee['type'],
                                    "entity": ee['entity']
                                })

                        D.append({
                            'text' : text1,
                            'entities' : entities1,
                        })
                        D.append({
                            'text' : text2,
                            'entities' : entities2,
                        })

                else:
                    D.append({
                        'text' : l['originalText'],
                        'entities' : entities
                    })

    #print(len(D))

    return D


if __name__ == '__main__':

    D_train = get_data('data/ccks2019/subtask1_training_part1.jsonl', False)
    D_train.extend( get_data('data/ccks2019/subtask1_training_part2.jsonl', False) )
    D_dev = get_data('data/ccks2019/subtask1_test_set_with_answer.jsonl', False)


    # 重新分割
    train_num = len(D_train)
    dev_num = len(D_dev)

    print(f"train: {train_num}\tdev: {dev_num}")

    new_dev_num = int((train_num + dev_num) * new_ratio)

    print(f"new train: {train_num+(dev_num-new_dev_num)}\tnew dev: {new_dev_num}")

    json.dump(
        D_train + D_dev[:-new_dev_num],
        open('dataset/ccks_train.json', 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )

    json.dump(
        D_dev[-new_dev_num:],
        open('dataset/ccks_dev.json', 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )

    json.dump(
        list(categories),
        open('data/ccks_categories.json', 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )
