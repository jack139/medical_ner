import json
import glob


def statistic(infile):
    count = {
        "检验和检查" : 0,
        "疾病和诊断" : 0,
        "症状和体征" : 0,
        "治疗和手术" : 0,
        "解剖部位" : 0,
        "药物" : 0,
    }

    for l in json.load(open(infile)):
        for e in l['entities']:
            count[e['type']] += 1

    print(infile)
    for k in count.keys():
        print(f"{k:6}:\t{count[k]}")

if __name__ == '__main__':
    file_list = glob.glob("dataset/*")
    for i in file_list:
        statistic(i)

    statistic('data/pack_train.json')
    statistic('data/pack_dev.json')