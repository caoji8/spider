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

d = [{"order": 3}, {"order": 1}, {"order": 2}]
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
