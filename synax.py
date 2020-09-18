from collections import defaultdict

# lamda 箭头函数
# b = lambda : True
two_sum = (lambda x, y: x + y)(3, 4)


# print(two_sum)   7

# 闭包
def sum(x):
    return lambda y: x + y


sum_with_100 = sum(100)
result = sum_with_100(200)

d = [{'order': 3}, {'order': 1}, {'order': 2}]
# 根据order键值排序
d.sort(key=lambda x: x['order'])


# print('aba' == 'aba'[::-1])

# print('aba'[0:2])
# IndentationError: unindent does not match any outer indentation level
#                       ^
#     elif strs < -2**31:
# Line 10  (Solution.py)


# （1）空为0，需要首先排除；
# （2）在进行一系列操作之前，需要将第一个非空字符之前所有的空格删去，删除过程要注意索引范围；
# （3）第一次出现正负号，还需要判断此正负号是否为第一个非空字符，若否，则停止；
# （4）若第一个非空字符是数字，后一个是除正负号以外的符号，则停止；
# （5）若第一个非空字符为正负号，紧接其后的必须是数字，否则无法生成有效数字；
# （6）第一个非空字符不是正负号或者数字，必定无法生成有效整数；
class Solution:
    def maxProfit(self, prices) -> int:
        _zero = prices[0:]
        _zero.sort(reverse=True)
        if prices == _zero:
            return 0
        elif prices == _zero[::-1]:
            return prices[-1] - prices[0]
        else:
            min_count = min(prices)
            prices = prices[prices.index(min_count):]
            count = 0

            if len(prices) % 2 == 0:
                for i in range(0, len(prices), 2):
                    count += prices[i + 1] - prices[i]
            else:
                prices.remove(prices[-1])
                for i in range(0, len(prices), 2):
                    count += prices[i + 1] - prices[i]
            return count


s = Solution()

# print(s.maxProfit([7, 1, 5, 3, 6, 4]))
# [7,1,5,3,6,4]

# a = defaultdict(int)
# a[1] += 1
# a[1] += 1
# print(a)


# import time
# a = time.time()
# time.sleep(3)
# b = time.time()
# print(int(b-a))

# def get_data():
#     for i in range(10):
#         print('in fun', i)
#         yield i

# nums = get_data()
# for i in nums:
#     print(i)


"""
list
1、cmp(list1, list2)：比较两个列表的元素 
2、len(list)：列表元素个数 
3、max(list)：返回列表元素最大值 
4、min(list)：返回列表元素最小值 
5、list(seq)：将元组转换为列表 
列表操作包含以下方法:
1、list.append(obj)：在列表末尾添加新的对象
2、list.count(obj)：统计某个元素在列表中出现的次数
3、list.extend(seq)：在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
4、list.index(obj)：从列表中找出某个值第一个匹配项的索引位置
5、list.insert(index, obj)：将对象插入列表
6、list.pop(obj=list[-1])：移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
7、list.remove(obj)：移除列表中某个值的第一个匹配项
8、list.reverse()：反向列表中元素
9、list.sort([func])：对原列表进行排序
"""

"""

dict
copy()浅拷贝字典
update(dict)添加不存在元素更新已有元素
pop(key) 删除指定键值对
popitem() 删除随机键值对
setdefault() 返回key的value if None return None

"""

