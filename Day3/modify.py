import sys
# 引入两个参数，第一个为想要修改的字符串，第二个为目标字符串
oldstr = sys.argv[1]
newstr = sys.argv[2]

with open("file1", "r", encoding="utf-8") as fr:
    with open("file1-new", "w", encoding="utf-8") as fw:
        for line in fr:
            if oldstr in line:
                line = line.replace(oldstr, newstr)
            fw.write(line)

