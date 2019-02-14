import json

dic1 = {
    "广州": {
        "花都": "001",
        "越秀": "002",
        "海珠": "003",
        "黄埔": "004"
    },
    "深圳": {
        "宝安": "011",
        "龙华": "012",
        "福田": "013"
    }
}

# json序列化
with open("json.dump", "w") as fw:
    print(json.dumps(dic1))
    fw.write(json.dumps(dic1))  # 等同于json.dump(dic1, fw)

# json反序列化
with open("json.dump", "r") as fr:
    data = json.loads(fr.read()) # 等同于json.load(dic1, fr)
    print(data)