import json

new_ratio = 0.1

categories = set()

def get_data(infile):
    D = json.load(open(infile))

    for d in D:
        for e in d['entities']:
            categories.add(e['type'])

    #print(len(D))
    return D


if __name__ == '__main__':

    D_train = get_data('data/CMeEE/CMeEE_train.json')
    D_dev = get_data('data/CMeEE/CMeEE_dev.json')

    # 重新分割
    train_num = len(D_train)
    dev_num = len(D_dev)

    print(f"train: {train_num}\tdev: {dev_num}")

    new_dev_num = int((train_num + dev_num) * new_ratio)

    print(f"new train: {train_num+(dev_num-new_dev_num)}\tnew dev: {new_dev_num}")

    json.dump(
        D_train + D_dev[:-new_dev_num],
        open('data/cmeee_train.json', 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )

    json.dump(
        D_dev[-new_dev_num:],
        open('data/cmeee_dev.json', 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )

    json.dump(
        list(categories),
        open('data/cmeee_categories.json', 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )
