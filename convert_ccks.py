import json

new_ratio = 0.1

categories = set()

def get_data(infile, include_blank=True):
    D = []

    with open(infile, encoding='utf-8') as f:
        for l in f:
            l = json.loads(l)

            entities = []
            for e in l['entities']:
                
                entities.append({
                    "start_idx": e['start_pos'],
                    "end_idx": e['end_pos']-1,
                    "type": e['label_type'],
                    "entity": l['originalText'][e['start_pos']:e['end_pos']]
                })

                categories.add(e['label_type'])

            if include_blank or len(entities)>0:
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
        open('data/ccks_train.json', 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )

    json.dump(
        D_dev[-new_dev_num:],
        open('data/ccks_dev.json', 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )

    json.dump(
        list(categories),
        open('data/ccks_categories.json', 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )