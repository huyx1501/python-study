import re

# match方法：匹配开头
print(re.match("[A-Z]+", "superMan666Super"))  # 无匹配项
print(re.match("[A-Z]+", "SSuperMan666Super"))  # 匹配SS
print(re.match("[A-Z]+", "SSuperMan666").group())  # 返回匹配到的字符串

# search方法：在字符串中搜索,返回第一个匹配到的字符串
print(re.search("[A-Z]+", "superMan666Super"))

# findall方法：返回所有匹配到的字符串
print(re.findall("[A-Z]+", "superMan666Super"))

# split方法：以匹配到的字符串分割字符串，返回一个列表
print(re.split("[A-Z]+", "superMan666Super"))

# sub方法：将匹配到的字符串替换为指定字符串
print(re.sub("[A-Z]+", "||", "superMan666Super"))

# 匹配模式re.I：忽略大小写
print("re.I".center(20, "="))
print(re.findall("[A-Z]+", "superMan666Super", re.I))

# 匹配模式re.M：多行匹配，
print("re.M".center(20, "="))
print(re.findall("[a-zA-z]+", "superMan\nSuper666"))
print(re.findall("^[a-zA-z]+", "superMan\nSuper666"))
print(re.findall("^[a-zA-z]+", "superMan\nSuper666", re.M))

# 匹配模式re.S：点任意匹配，贪婪模式
print("No re.S".center(20, "="))
print(re.search(".+", "superMan\n666Super").group())
print("re.S".center(20, "="))
print(re.search(".+", "superMan\n666Super", re.S).group())

# 反斜杠匹配
print(re.search("\\\\", "123\\456").group())  # 四个放斜杠两两一组python经解析器后成两个反斜杠，最后再经一次re转义后还原成一个反斜杠
print(re.search(r"\\", "123\\456").group())  # 使用python原生字符串模式，两个反斜杠由re转义成为一个字符串类型的反斜杠
print(re.search(r"\\", r"123\456").group())  # 前后都使用原生字符串

# 分组匹配：将匹配到的字符串分组存为一个K/V对，然后组合成一个字典
print(re.search("(?P<area>[0-9]{3,4})-(?P<number>[0-9]{7,8})", "010-12345678").groupdict())