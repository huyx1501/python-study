# -*- coding:utf-8-*-
s = "你好"
print("coding:", s)

# s_unicode =s.decode("gbk") python2
s_unicode = s
print("unicode:", s_unicode)

s_gbk = s_unicode.encode("gbk")
print("gbk:", s_gbk)

s_utf8 = s_gbk.decode("gbk").encode("utf-8")
print("utf-8:", s_utf8)

s_gb2312 = s_utf8.decode("utf-8").encode("gb2312")
print("gb2312:", s_gb2312)

