
def query_node(_node_name):
    # 以只读方式打开配置文件
    with open("config.cfg", "r", encoding="utf-8") as f:
        for line in f:
            if ("backend %s" % _node_name).strip() == line.strip():
                # 如果匹配上节点标题，就返回下一行记录
                return f.readline()
        else:
            return "节点不存在"


def add_node(_node_name, _server, _weight, _maxconn):
    # 拼凑标题
    _node_title = "\nbackend %s\n" % _node_name
    # 拼凑配置内容
    _node_info = "\tserver %s weight %s maxconn %s" % (_server, _weight, _maxconn)
    # 以读写方式打开配置文件
    with open("config.cfg", "r+", encoding="utf-8") as f:  # 坑：a+ 模式为什么不行
        for line in f:
            # 如果标题以及存在则不允许新增
            if _node_title.strip() == line.strip():
                return "节点已存在，不允许重复添加"
        else:
            f.write(_node_title)
            f.write(_node_info)
            return "添加节点成功"


def del_node(_node_name, _server, _weight, _maxconn):
    _node_title = "\nbackend %s\n" % _node_name
    _node_info = "\tserver %s weight %s maxconn %s" % (_server, _weight, _maxconn)
    # 以只读方式打开文件并读取所有行到一个列表中
    with open("config.cfg", "r", encoding="utf-8") as f, open("config.cfg.bak", "w", encoding="utf-8") as fb:
        newlines = f.readlines()
        fb.writelines(newlines)  # 备份文件
    with open("config.cfg", "w", encoding="utf-8") as fw:
        # 确定列表中是否存在匹配的标题
        if _node_title.lstrip() in newlines:
            # 确定标题在列表中的位置
            title_index = newlines.index(_node_title.lstrip())
            # 标题的下一个位置为内容的位置
            info_index = title_index + 1
            # 如果内容匹配则把列表中匹配的标题和内容进行移除
            if _node_info.strip() == newlines[info_index].strip():
                newlines.pop(info_index)
                newlines.pop(title_index)
                fw.writelines(newlines)
                return "删除节点成功"
            else:
                # 内容不匹配直接写入原来的内容
                fw.writelines(newlines)
                return "指定的节点内容不匹配"
        else:
            # 标题不匹配时直接写入原来的内容
            fw.writelines(newlines)
            return "没有匹配的节点"


# 操作选择
ops = ("query", "add", "delete")
for op in ops:
    print(op)
option = input("请选择操作类型：")

if option == "query":
    node_name = input("请输入要查询的节点名：")
    print(query_node(node_name))

elif option == "add":
    node_info = input("请输入要添加的节点信息：")
    # 还原输入成KV模式，并提取其中的节点标题和配置内容
    node_name = eval(node_info)["backend"]
    record = eval(node_info)["record"]
    print(add_node(node_name, record["server"], record["weight"], record["maxconn"]))

elif option == "delete":
    node_info = input("请输入要删除的节点信息：")
    node_name = eval(node_info)["backend"]
    record = eval(node_info)["record"]
    print(del_node(node_name, record["server"], record["weight"], record["maxconn"]))

else:
    print("Input error!")
    exit(1)
