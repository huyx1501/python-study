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

dic1["深圳"]["南山"] = "014"
dic1["广州"]["黄埔"] = "005"

print(dic1)
