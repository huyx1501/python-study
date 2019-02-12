
with open("file2", "r") as fr:
    print(fr.read())
    print(fr.tell())
    fr.seek(0)
    print("read2:\n", fr.read())


with open("file2", "w") as fw:
    fw.write("Hello\n")

with open("file2", "a") as fa:
    fa.write("World\n")

with open("file2", "r+") as frp:
    # 读取一行
    print("frp:\n", frp.readline().strip())
    # 追加一行
    frp.write("============")
    # 读取剩余行
    print("frp2:\n", frp.read())

with open("file3", "w+") as fwp:
    fwp.write("============\n")
    fwp.write("Hello world\n")
    fwp.flush()
    print(fwp.read())  # 没用

with open("file3", "ab+") as fap:
    fap.write("============\n".encode())
    fap.write("Hello world\n".encode())
    print(fap.read())   # 没用
