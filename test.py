n, k = map(int, input().split())
attribute_sums = {}  # 用于存储属性之和的哈希表
print(n,k)

# 输入物品的属性并计算属性之和
for i in range(n):
    attributes = list(map(int, input().split()))
    attr_sum = sum(attributes)
    if attr_sum in attribute_sums:
        attribute_sums[attr_sum] += 1
    else:
        attribute_sums[attr_sum] = 1

perfect_pairs = 0

# 遍历每个物品，查找完美对
for i in range(n):
    target_sum = i + 1  # 计算目标属性之和
    if -target_sum in attribute_sums:
        perfect_pairs += attribute_sums[-target_sum]

print(perfect_pairs)
