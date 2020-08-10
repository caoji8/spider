import json
with open('data.json','r',encoding='utf-8') as load_f:
    load_dict = json.load(load_f)
    num_image = len(load_dict)
    for image in range(num_image):
        name = load_dict[image]['name']
        price = load_dict[image]['price']
        print(name)
        print(price)
