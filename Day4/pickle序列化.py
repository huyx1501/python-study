import pickle

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
    },
    "iter1": iter([1, 2, 3, 4])  # 迭代器对象
}

# pickle序列化
with open("pickle.dump", "wb") as fw:
    print(pickle.dumps(dic1))
    fw.write(pickle.dumps(dic1))  # 等同于pickle.dump(dic1, fw)

# pickle反序列化
with open("pickle.dump", "rb") as fr:
    data = pickle.loads(fr.read())  # 等同于pickle.load(dic1, fr)
    print(data)
    # 还原迭代器对象并调用其__next__方法
    print(data["iter1"].__next__())
    print(data["iter1"].__next__())
