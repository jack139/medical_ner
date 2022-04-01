# 医学文本命名实体识别数据合集



## 数据来源

- CCKS 2019
- CMeEE
- CMeIE
- IMCS
- MedDG



## 数据格式转换

```shell
python3 imcs_split.py
python3 convert_imcs.py
python3 convert_cmeee.py
python3 convert_cmeie.py
python3 convert_ccks.py
python3 convert_meddg.py
```



## 训练

```shell
python3 baseline_train.py
```



## 标签合并
```
                    CMeEE     CMeIE       CCKS            IMCS                   MedDG
    "检验和检查"     "ite",    "检查"       "实验室检验"   "Medical_Examination"    "Test"
                                          "影像检查"
 X  "医疗设备"       "equ",     
    "疾病和诊断"     "dis",    "疾病"       "疾病和诊断"                           "Disease"
    "症状和体征"     "sym",    "症状"                     "Symptom"
 X  "微生物类"       "mic",     
    "治疗和手术"     "pro",    "手术治疗"    "手术"        "Operation"
                              "其他治疗"
 X  "科室"           "dep",     
    "解剖部位"        "bod",   "部位"       "解剖部位"
    "药物"           "dru"     "药物"       "药物"         "Drug"                "Medicine"
                                                       "Drug_Category"
 X  "流行病学"                 "流行病学",
 X  "社会学"                   "社会学",
 X  "预后"                     "预后",
 X  "其他"                     "其他",
```



## 数据统计

| 数据集 | train | dev  | baseline |
| ------ | ----- | ---- | -------- |
| CCKS   | 1241  | 137  |          |
| CMeEE  | 17588 | 1954 |          |
| CMeIE  | 13899 | 1544 |          |
| IMCS   | 35889 | 3771 |          |
| MedDG  | 52361 | 5817 |          |
| 合集   |       |      |          |

