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
python3 pack.py
```



## 训练

```shell
python3 baseline_train.py
```



## 标签合并
|   合并标签   | CMeEE |       CMeIE        |      CCKS 2019       |        IMCS         |  MedDG   |
| :----------: | :---: | :----------------: | :------------------: | :-----------------: | :------: |
|  检验和检查  |  ite  |        检查        | 实验室检验，影像检查 | Medical_Examination |   Test   |
|  疾病和诊断  |  dis  |        疾病        |      疾病和诊断      |                     | Disease  |
|  症状和体征  |  sym  |        症状        |                      |       Symptom       |          |
|  治疗和手术  |  pro  | 手术治疗、其他治疗 |         手术         |      Operation      |          |
|   解剖部位   |  bod  |        部位        |       解剖部位       |                     |          |
|     药物     |  dru  |        药物        |         药物         | Drug, Drug_Category | Medicine |
| ~~医疗设备~~ |  equ  |                    |                      |                     |          |
| ~~微生物类~~ |  mic  |                    |                      |                     |          |
|   ~~科室~~   |  dep  |                    |                      |                     |          |
| ~~流行病学~~ |       |      流行病学      |                      |                     |          |
|  ~~社会学~~  |       |       社会学       |                      |                     |          |
|   ~~预后~~   |       |        预后        |                      |                     |          |
|   ~~其他~~   |       |        其他        |                      |                     |          |



## 数据统计

| 数据集 | train | dev  | baseline |
| :----: | :---: | :--: | :------: |
| CCKS 2019 | 1310  | 327  | 84.638 |
| CMeEE  | 17588 | 1954 | 65.281 |
| CMeIE  | 13899 | 1544 | 77.592 |
| IMCS   | 35889 | 3771 | 92.751 |
| MedDG  | 52361 | 5817 | 99.571 |
| pack 合集 | 121047 | 13413 | 82.966 |



## 标签统计

|   label    | pack_train | pack_dev | baseline |
| :--------: | :--------: | :------: | :------: |
| 检验和检查 |   36187    |   4298   |  85.329  |
| 疾病和诊断 |   99982    |  11565   |  84.719  |
| 症状和体征 |   63112    |   7154   |  77.411  |
| 治疗和手术 |   13949    |   1379   |  65.301  |
|  解剖部位  |   31870    |   5160   |  75.007  |
|    药物    |   58141    |   6763   |  93.742  |

