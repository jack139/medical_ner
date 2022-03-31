import os
import json

orgin_path = 'data/IMCS-NER'
new_path = 'data/IMCS-NER/new_split'

train_file = "IMCS_train.json"
dev_file = "IMCS_dev.json"

new_ratio = 0.1

train_data = json.load(open(os.path.join(orgin_path, train_file)))
dev_data = json.load(open(os.path.join(orgin_path, dev_file)))

train_num = len(train_data)
dev_num = len(dev_data)

print(f"train: {train_num}\tdev: {dev_num}")


# 重新分割
new_dev_num = int((train_num + dev_num) * new_ratio)

for i in [k for k in dev_data.keys()][:-new_dev_num]:
	train_data[i] = dev_data[i]
	dev_data.pop(i)


json.dump(
    train_data,
    open(os.path.join(new_path, train_file), 'w', encoding='utf-8'),
    indent=4,
    ensure_ascii=False
)

json.dump(
    dev_data,
    open(os.path.join(new_path, dev_file), 'w', encoding='utf-8'),
    indent=4,
    ensure_ascii=False
)

print(f"new train: {len(train_data)}\tnew dev: {len(dev_data)}")