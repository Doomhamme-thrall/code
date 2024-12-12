# import random
#
# i = int(input("Enter a number: "))
# j = random.randint(1, 99)
# k = 1
#
# while i != j:
#     if i < j:
#         print("too small")
#     else:
#         print("too big")
#     i = int(input("Enter another number: "))
#     k += 1
# else:
#     print("good")
#     print("total guessed", k, "times")
#
# a = 1;
# b = 2;
# c = 3;
# d = 4;
# e = 5;
# f = 6;
# 应分行
# print(a)
#
# 关键字
# import keyword
#
# print(keyword.kwlist)
#
# x = 1
# print(x)
# del x
# print(type(x))
#
# 交换变量
# a = "abc"
# b = "xyz"
# print(a, b)
# a, b = b, a
# print(a, b)
#
# 运算符
# a = "a"
# b = "C"
# print(a + b)
# print(a * b)
# print(a / b)
# print(a // b)
# print(a % b)
# print(a ** b)
#
# print(a == b)
# print(a != b)
# print(a > b)
# print(a < b)
# print(a >= b)
# print(a <= b)

# 逻辑运算符 and or not
# c = True
# d = False
# print(not (c and d))
#
# 位运算 & 位与 | 位或
#
# a = 20
# b = 39
# print(a & b)
# print(a | b)
#
# 成员运算符 in / not in
# a = "string"
# i = [2, 3, 4, 5, 89, 11, 999, "string"]
# print(a in i)

# 身份运算符 is:判断地址是否相等（==判断数值是否相等）   is not
# a=[1,2,3]
# b=[1,2,3]
# c=[4,5,6]
# print(a is b)
# print(a is not c)
# print(a==b)
# b=a
# print(a is b)

import math

r = int(input("Enter r: "))
s = 4 * math.pi * r**2
print(s)
v = 4 / 3 * math.pi * r**3
print(v)
