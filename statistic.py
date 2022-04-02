import json
import glob


def statistic_label(infile):
    count = {
        "检验和检查" : 0,
        "疾病和诊断" : 0,
        "症状和体征" : 0,
        "治疗和手术" : 0,
        "解剖部位"   : 0,
        "药物"      : 0,
    }

    for l in json.load(open(infile)):
        for e in l['entities']:
            count[e['type']] += 1

    print(infile)
    for k in count.keys():
        print(f"{k:6}:\t{count[k]}")


def statistic_label_value(infile):
    count = {
        "检验和检查" : set(),
        "疾病和诊断" : set(),
        "症状和体征" : set(),
        "治疗和手术" : set(),
        "解剖部位"   : set(),
        "药物"      : set(),
    }

    for l in json.load(open(infile)):
        for e in l['entities']:
            count[e['type']].add(e['entity'])

    print(infile)
    for k in count.keys():
        #count[k] = list(count[k])
        print(f"{k:6}:\t{len(count[k])}")

    return count


if __name__ == '__main__':
    #file_list = glob.glob("dataset/*")
    #for i in file_list:
    #    statistic_label(i)

    statistic_label('data/pack_train.json')
    statistic_label('data/pack_dev.json')

    c1 = statistic_label_value('data/pack_train.json')
    c2 = statistic_label_value('data/pack_dev.json')

    print("")
    for k in c1.keys():
        print(k, len(c2[k] | c1[k]), len(c2[k] - c1[k]))
        c1[k] = list(c1[k])

    #json.dump(
    #    c1,
    #    open('data/pack_stat.json', 'w', encoding='utf-8'),
    #    indent=4,
    #    ensure_ascii=False
    #)
