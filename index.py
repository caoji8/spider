import requests
import html
# url = 'https://tieba.baidu.com/f?kw=bilibili&fr=index'
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                          "Chrome/81.0.4044.122 Safari/537.36",
#            }
# params = {
#     "kw": "bilibili",
#     "fr": 'index'
# }
# response = requests.get(url,headers=headers)
#
# assert response.status_code == 200
#
# print(response.text)

# Cookie = {'Cookie': 'PHPSESSID=dt22qgpcpculvpmilisj6vlku6'}
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
#
# url = 'http://210.28.144.20:206/browse/cls_browsing_tree.php?s_doctype=all&cls=A1&lvl=1'
# s = 'http://210.28.144.20:206/browse/cls_browsing_book.php?s_doctype=all&cls=A3'
# response = requests.get(s,headers=headers,cookies=Cookie)
# res = response.content.decode('utf-8')
# # searchF('A1','%26%23x9a6c%3B%26%23x514b%3B%26%23x601d%3B%26%23x3001%3B%26%23x6069%3B%26%23x683c%3B%26%23x65af%3B%26%23x8457%3B%26%23x4f5c%3B')
# print(html.unescape(res))

import sys

sys.setrecursionlimit(1000000)
def fact(n):

    return fact_iter(n, 1)


def fact_iter(num, product):
    print(num)
    if num == 1:
        return product
    return fact_iter(num - 1, num * product)
fact(3930)
