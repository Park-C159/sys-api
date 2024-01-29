# 创建一个字典，用于存储属性之和的频率统计，字典的键是属性之和，值是该属性之和出现的次数。
#
# 遍历每个物品，对每个物品，计算其属性之和，并将结果保存到字典中，同时增加对应属性之和的频率计数。
#
# 遍历每个物品，对每个物品，计算目标属性之和，即i^2 - (该物品的属性之和)。
#
# 查找目标属性之和在字典中的频率。如果该频率大于等于2，说明存在至少两个物品的属性之和等于目标属性之和，即存在完美对。
#
# 统计所有具有至少两个相同属性之和的物品的数量。
#
# 返回统计结果作为完美对的个数。
def is_perfect_pair(item1, item2):
    return sum(item1) == sum(item2)

def count_perfect_pairs(n, k, items):
    perfect_pairs = 0

    for i in range(n):
        for j in range(i+1, n):
            if is_perfect_pair(items[i], items[j]):
                perfect_pairs += 1

    return perfect_pairs

n, k = map(int, input().split())
items = [list(map(int, input().split())) for _ in range(n)]

result = count_perfect_pairs(n, k, items)
print(result)

