import json
import glob


labels = [
        "检验和检查",
        "疾病和诊断",
        "症状和体征",
        "治疗和手术",
        "解剖部位",
        "药物",
]

def evaluate(infile):
    X, Y, Z = 1e-10, 1e-10, 1e-10

    for l in json.load(open(infile)):
        T = len(l['entities'])
        B = 0
        for e in l['entities']:
            if e.get('predict')=='bingo':
                B += 1
        R = B + len(l['entities_pred'])
        X += B
        Y += R
        Z += T
    f1, precision, recall = 2 * X / (Y + Z), X / Y, X / Z

    return f1, precision, recall

def evaluate_by_label(infile, label):
    X, Y, Z = 1e-10, 1e-10, 1e-10

    for l in json.load(open(infile)):
        T = 0
        B = 0
        for e in l['entities']:
            if e['type']==label:
                T += 1
                if e.get('predict')=='bingo':
                    B += 1
        R = B
        for e in l['entities_pred']:
            if e['type']==label:
                R += 1
        X += B
        Y += R
        Z += T
    f1, precision, recall = 2 * X / (Y + Z), X / Y, X / Z

    return f1, precision, recall


if __name__ == '__main__':
    for label in labels:
        f1, precision, recall = evaluate_by_label('data/pack_dev_pred.json', label)
        print(f"{label:6}\tF1: {f1:.5f}\tP: {precision:.5f}\tR: {recall:.5f}")

    f1, precision, recall = evaluate('data/pack_dev_pred.json')
    print(f"All leabels\tF1: {f1:.5f}\tP: {precision:.5f}\tR: {recall:.5f}")
