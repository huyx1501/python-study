import xml.etree.ElementTree as E

# 读取xml文档
xml_tree = E.parse("data_example.xml")

# 获取xml文档的根元素
root = xml_tree.getroot()
print(root)
print("root.tag:", root.tag)

# 遍历xml文档
for leaf in root:
    # 获取节点tag名称
    print("leaf.tag:", leaf.tag)
    # 获取节点属性
    print("leaf.attrib:", leaf.attrib)
    # 获取节点值
    print("leaf.text:", leaf.text)
    # 遍历下一层
    for n in leaf:
        print(n)
        print(n.text)

print("==================================")
# 修改节点
# 循环查找出所有year节点
for leaf in root.iter("year"):
    print(leaf.text)
    # 修改节点内容（要转换成字符串）
    leaf.text = str(int(leaf.text) + 1)
    # 增加属性
    leaf.set("mod", "true")
# 写入到文件
xml_tree.write("data_example_mod.xml")

print("==================================")
# 查找所有country节点
for leaf in root.findall("country"):
    # 从country节点查找year子节点
    year = int(leaf.find("year").text)
    if year < 2017:
        # remove 方法删除节点
        root.remove(leaf)

xml_tree.write("data_example_mod2.xml")

# ===========创建xml========
# 创建根元素
info = E.Element("info")
# 创建子元素，指定上级元素，指定元素属性
name = E.SubElement(info, "person", name="Bob")
age = E.SubElement(name, "age")
# 为子元素赋值
age.text = "20"
sex = E.SubElement(name, "sex")
sex.text = "Male"

# 第二个子元素
name2 = E.SubElement(info, "person", name="Tiny")
age2 = E.SubElement(name2, "age")
age2.text = "30"
sex2 = E.SubElement(name2, "sex")
sex2.text = "Female"

# 生成元素树
el = E.ElementTree(info)
# 写入文件
el.write("new_xml.xml")