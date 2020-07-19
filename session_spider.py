import requests

session = requests.session()
post_url = "http://www.renren.com/PLogin.do"
post_data = {
    "email": "mr_mao_hacker@163.com",
    "password":"alarmchime"
}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}

# session发送post后cookie自动保存再变量中
session.post(post_url,data=post_data,headers=headers)
r = session.get('http://www.renren.com/327550029/profile',headers=headers)

print(r.content.decode())
