import re

str = 'hello\nhelloworldsjaoifdwoei'
a = re.findall(r'hello',str,re.DOTALL)
print(a)
