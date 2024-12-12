# # 显式定义元组
# tuple1 = (1, 2, 3, 4, 5)
# print(tuple1)
# tuple2 = 1, 2, 3, 4, tuple1
# print(tuple2)
# print(tuple2[4][1])
# print(tuple2.index(4))  # 指定值第一次出现位置
# print(tuple2.count(4))  # 计数


# single = 1
# print(single)
# single_new = (1,)  # 逗号，单个元素的元组
# print(single_new)

# a, b = 1, 2  # 多变量同步赋值
# print(a, b)
# a, b = b, a
# print(a, b)

# import math

# for i, j in [(1, 2), (3, 4), (5, 6)]:
#     print(math.hypot(i**2 + j**2))


# ls = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# tuplist = tuple(ls)
# print(tuplist, type(tuplist))
# tuplist = list(tuplist)
# print(tuplist, type(tuplist))

# 定义集合
# st = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
# print(type(st))
# st = {1, 1, 9, 3, 4, 5, 6, 9}
# print(type(st))
# print(st)

# st.add(10)
# print(st)
# st.add(1)
# print(st)
# st.update([11, 12, 13])
# print(st)
# st.update("hello")
# print(st)
# st.discard("hello")  # 删除不存在的元素不会报错
# print(st)
# st.clear()
# print(st)

# 交并集
# set1 = {1, 2, 3, 4, 5}
# set2 = {4, 5, 6, 7, 8}
# print(set1 & set2)
# print(set1 | set2)
# print(set1.intersection(set2))
# print(set1.union(set2))

# a = {1, 2, 3, 4, 5}
# b = {1, 2, 3, 4, 5, 6}
# print(a.issubset(b))
# print(b.issuperset(a))
# print(a.isdisjoint(b))

# 字典
# dict1 = {"a": 1, "b": 2, "c": 3}
# print(dict1["a"])
# print(dict1["b"])  # keyerror
# print(dict1.get("a"))
# dict1["a"] = 17
# print(dict1["a"])
# del dict1["a"]
# print(dict1)

# print(dict1.pop("b"))
# print(dict1)
# del dict1

# import copy

# dict1 = {"a": 1, "b": 2, "c": 3}
# dict2 = copy.copy(dict1)
# dict1["a"] = 17
# print(dict1)
# print(dict2)
# print(id(dict1), id(dict2))

# dict1 = {"a": 1, "b": 2, "c": 3}
# for i in dict1:
#     print(i, dict1[i])

