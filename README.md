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
```



## 训练

```shell
python3 baseline_train.py
```

