names = ["ZhangSan", "LiSi", "WangWu", "ZhaoLiu"]
'''
#列表切片
print(names)  #打印列表
print(names[2])  #打印列表第三个元素
print(names[0:3])  #打印第1-4个元素开头位置之间的元素
print(names[:3])  #打印从开头到第四个元素开头位置的元素
print(names[-3:-1])  #打印倒数第三到倒数第一个元素开头位置的元素
print(names[-2:])  #打印倒数第二个元素开头到最后一个元素结尾位置的元素
'''
#列表操作
_names = ["Alex",["AAA", "BBB"],"LiSi"]  #列表嵌套
names.extend(_names)  #追加新列表到当前列表尾端
names.append("HuHu")  #在列表末尾追加元素
names.insert(1,"YangYang")  #在列表指定位置插入元素
names.pop(0)  #删除指定位置的元素
names.remove("WangWu")  #删除指定的元素内容
names2 = names.copy()  #复制列表
names[2]="WangWang"  #修改指定位置的元素
names[names.index(["AAA", "BBB"])][0]="CCC"  #修改嵌套列表指定元素(对浅Copy会同样修改)
print(names.index("Alex"))  #列出指定元素所在的位置
print(names.count("LiSi"))   #统计指定元素在列表中的数量
print(names2)
print(names.reverse())  #反转列表，注意，没有返回值!
print(names)

