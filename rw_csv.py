import pandas as pd

# plan 1
a = [1, 2, 3]
b = [4, 5, 6]
dataframe = pd.DataFrame({'name': a, 'age': b})

[0,1].to_csv('test.csv',index=False,sep=',',mode='a')
# dataframe.to_csv('test.csv',mode='a')
print(pd.read_csv('test.csv'))

# plan 2
# import csv
# with open('test.csv', 'w') as csvfile:
#     writer = csv.writer(csvfile)
#     # 首行
#     writer.writerow(['index', 'name', 'age'])
#     # 执行多行
#     writer.writerows([[0, 1, 3], [0, 1, 3], [0, 1, 3]])

# with open('test.csv', 'r') as csvfile:
#     reader = csv.reader(csvfile)
#
#     for line in reader:
#         print(line)



# r = map(lambda x: x*x , [1,2,3,4,5,6,7])
# print(list(r))

