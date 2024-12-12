# x1, y1, x2, y2 = eval(
#     input("Enter the coordinates of two points separated by commas: ")
# )
# distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
# print("The distance between the two points is", distance)

# 选择结构
# 单分支
# age = int(input("请输入年龄："))
# if age >= 18:
#     print("成年")
# print("pass")

# 双分支
# age = int(input("请输入年龄："))
# if age >= 18:
#     print("成年")
# else:
#     print("未成年")

# name = input("请输入姓名：")
# print(name, "成年" if int(input("请输入年龄：")) >= 18 else print("未成年"))

# # 多条件
# score_py = 80
# score_java = 70
# if score_py >= 60 and score_java >= 60:
#     print("通过")
# else:
#     print("不通过")

# bool1 = True
# if not bool1:
#     print("True")
# else:
#     print("False")

# 多分支
# score = (
#     int(input("请输入分数：")) + int(input("请输入分数：")) + int(input("请输入分数："))
# ) // 3
# if score >= 90:
#     print("一等奖")
# elif score >= 80:
#     print("二等奖")
# elif score >= 60:
#     print("三等奖")

# 选择结构
# sex = input("请输入性别：")
# age = int(input("请输入年龄："))
# if sex == "male":
#     if age >= 22:
#         print("到达合法婚龄")
#     else:
#         print("未到达合法婚龄")
# else:
#     if age >= 20:
#         print("到达合法婚龄")
#     else:
#         print("未到达合法婚龄")

# merry_age = 22 if sex == "male" else 20
# if age >= merry_age:
#     print("到达合法婚龄")

# # 循环
# num = 1
# while num <= 1000:
#     if num % 3 == 0 and num % 7 == 0:
#         print(num)
#     num += 1

# fruit = "banana"
# for i in range(len(fruit)):
#     print(fruit[i], end="")
# cnt = 0
# for i in range(1001):
#     if i % 3 == 0 and i % 7 == 0:
#         print(i)
#         cnt += 1
# print(cnt, "in total")

# for row in range(1, 10):
#     for col in range(1, row + 1):
#         print("*", end="")
#     print()

# for i in range(1, 10):
#     for j in range(1, i + 1):
#         print(f"{j}*{i}={i*j}", end="\t")
#     print()

# for i in range(1, 10):
#     for j in range(1, 13):
#         k = 36 - i - j
#         if 4 * i + 3 * j + k / 2 == 36:
#             print(i, j, k)

# for i in range(3):
#     n = 1
#     while n <= 10:
#         if n > 5:
#             break
#         print(n)
#         n += 1
# print("over")

# for letter in "Python":
#     if letter == "h":
#         pass
#         print("this is pass block")
#     else:
#         print(letter)
# print("over")

# xl = [1, 2, 3, 4, 5]
# yl = xl
# yl[0] = 6
# print(xl, yl)

# ls = [1, 2, 3, 4, 5]
# ls[1:3] = [5, 6, 2, 6, 7, 8]
# print(ls)
# ls[1:3] = []
# print(ls)

# animals = ["cat", "dog", "tiger", "lion"]
# animals.append("elephant")  # 在列表末尾追加新元素
# print(animals)
# animals.extend(animals)  # 在列表末尾一次性追加另一个序列中的多个值
# print(animals)
# animals.insert(1, "monkey")  # 在指定位置插入元素
# print(animals)
# animals.remove("cat")  # 删除第一个匹配的元素
# print(animals)
# animals.pop()  # 删除指定位置的元素
# print(animals)
# print(animals.count("tiger"))  # 统计某个元素在列表中出现的次数
# print(animals)
# animals.clear()  # 清空列表
# print(animals)
# del animals


# ls = [1, 4, 3, 3, 2, 5, 6, 7, 8, 9]
# ls.sort()
# print(ls)
# ls.sort(reverse=True)
# print(ls)
# ls.reverse()
# print(ls)

# square = [x**2 for x in range(10)]
# print(square)
