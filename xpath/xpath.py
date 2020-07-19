# coding=utf-8
from lxml import etree
import html


with open('xpath.html', 'r', encoding='utf-8') as r:
    f = r.read()
    ht = etree.HTML(f)
    # etree.tostring()字符串显示html return byte
    # lxml能修正html 但会过度修正

    # print(html.unescape(etree.tostring(ht).decode('utf-8')))

    ret1 = ht.xpath('//h3//a[@class="l"]/text()')
    price = ht.xpath('//small[@class="fade"]/text()')
    new_data = [{"name":i,"price":float(price[ret1.index(i)])} for i in ret1]
    print(new_data)
    # print(html.unescape(etree.tostring(ret1).decode('utf-8')))
    # print([html.unescape(etree.tostring(i).decode('utf-8')) for i in ret1])
