import os
import json


text_map = {
    '雷呗' : ['雷贝拉唑', '雷贝拉挫', '雷贝'],
    '胃炎' : ['胃肠炎', '胃肠到炎症', '胃部轻微炎症', '肠胃有炎症', '胃食管炎', '胃部有炎症',
        '胃十二指肠炎', '胃里炎症', '胃肠道炎症', '胃窦炎', '胃潴留', '胃部炎症', '胃豆炎', '胃发炎',
        '胃有炎症', '胃淋巴结炎', '胃窦粘膜慢性炎', '胃溃疡', '胃窦糜烂性炎', '胃窦黏膜慢性炎', '胃部有轻微炎症',
        '胃粘膜炎症', '胃糜烂胆襄炎', '胃黏膜炎', '胃底炎', '胃急性炎症', '胃内炎症', '胃肠道的急性炎症',
        '胃窦有点炎症', '胃肠都有炎症', '胆汁反流糜烂性胃药炎', '胃有点炎症', '胃的炎症', '胃内有炎症', 
        '胃内已经有炎症', '胃还有炎症', '胃腸炎', '胃肠道有炎症', '胃窦有点发炎', '胃窦部炎症'],
    '肠炎' : ['肠胃炎', '十二指肠溃疡', '肠道炎症', '胃肠到炎症', '肠道慢性炎症', '肠道炎',
        '肠道有炎症', '肠道消炎', '肠胃有炎症', '十二指肠球部炎症', '肠黏膜的炎症', '十二指肠球炎', 
        '十二肠球炎', '肠系膜淋巴结炎', '肠溃疡或炎症', '十二指肠的炎症', '肠道的炎症', '结肠慢性炎症',
        '十二支肠球炎', '十二指肠球部溃疡', '糜烂性十二指肠降段炎', '结肠脾区炎症', '肠系淋巴结炎', '肠梗阻', 
        '肠胃急性炎症', '直肠黏膜慢性炎', '盲肠憩室炎', '十二指肠球体炎', '肠发炎', '肠溶发炎',
        '肠道的急性炎症', '肠道轻微的炎症', '肠道有些炎症', '胃肠都有炎症', '十二指肠的部位的炎症', '肠胃有点炎症',
        '肠子发炎', '肠道肠黏膜炎症', '胃十二指肠疾病', '十二指肠求炎', '十二指肠黏膜有炎症', '结肠有炎症', 
        '肠有炎症', '肠系膜炎', '肠道有点炎症', '肠淋巴结炎', '结肠的炎性疾病', '结肠粘膜的炎症', 
        '肠道的慢性炎症', '肠道方面的炎症', '结肠的炎症'],
    '胆囊炎' : ['胆囊发炎', '胆囊有炎症', '胆囊有发炎', '胆囊周围炎', '胆囊处的炎症', '胆囊轻度发炎',
        '胆囊有点慢性炎症'],
    '阑尾炎' : ['阑尾发炎', '阑尾周围炎性粘连'],
    '培菲康' : ['双歧杆菌三联活菌胶囊'],
    '肠易激综合征' : ['肠易激'],
    '食管炎' : ['食道炎'],
    '藿香正气丸' : ['藿香正气'],
    '奥美拉唑' : ['奥美'],
    '雷贝拉唑' : ['雷贝'],
    '乳酸菌素片' : ['乳酸菌素'],
}

categories = [
    'Medicine',
    'Test',
    'Disease'
]

new_ratio = 0.1

cate_map = {
    "Test"     : "检验和检查",
    "Disease"  : "疾病和诊断",
    "Medicine" : "药物",
}

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

    data = json.load(open(infile))

    for d in data:
        for l in d:

            text = l['Sentence']            
            entities = []

            for c in categories:
                for e in l[c]:
                    s_idx = search(e, text)
                    if e=='奥美':
                        e = '奥美拉唑'
                    elif e=='雷贝':
                        e = '雷贝拉唑'
                    elif e=='乳酸菌素':
                        e = '乳酸菌素片'

                    if s_idx == -1:
                        if e == '便秘':
                            continue

                        if e in text_map.keys():
                            for x in text_map[e]:
                                s_idx = search(x, text)

                                if s_idx != -1:
                                    e = x
                                    break
                            if s_idx==-1:
                                #print('fail: ', s_idx, text, e) # 未找到
                                continue
                        else:
                            #print('fail: ', s_idx, text, e) # 未找到
                            continue

                    entities.append({
                        "start_idx": s_idx,
                        "end_idx": s_idx + len(e) - 1,
                        "type": cate_map[c],
                        "entity": e,
                    })

            # 加入数据集
            if include_blank or len(entities)>0:
                D.append({
                    'text' : text,
                    'entities' : entities,
                })


    return D


if __name__ == '__main__':

    D_train = get_data('data/MedDG/MedDG_train.json', False)

    # 重新分割
    train_num = len(D_train)

    print(f"all: {train_num}")

    new_dev_num = int(train_num * new_ratio)

    print(f"new train: {train_num-new_dev_num}\tnew dev: {new_dev_num}")

    json.dump(
        D_train[:-new_dev_num],
        open('dataset/meddg_train.json', 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )

    json.dump(
        D_train[-new_dev_num:],
        open('dataset/meddg_dev.json', 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )


    json.dump(
        list(categories),
        open('data/meddg_categories.json', 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )
