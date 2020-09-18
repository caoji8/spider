import requests
import execjs
import sys


# 功能
# 获取语言类型
# 发送post请求返回响应&携带语言类型&携带数据
# 获取响应
# 提取翻译结果

def get_sign(input_str):
    with open('baidujs.js','r') as f:
        jsData = f.read()
    sign = execjs.compile(jsData).call('e', input_str)
    return sign


class BaiduTranslate(object):
    def __init__(self, input_str):
        self.input_str = input_str
        self.token = 'ce90b7b40d6f5ecb81e8c7d1fc2d4397'
        self.header = {"User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36"}
        self.url = 'https://fanyi.baidu.com/basetrans'
        self.cookies = {'Cookie':'MCITY=-347%3A; BDUSS=BRUnNLbTJ1MDlRWDlua1VYRWtpRFNLMmZjTUcyNXMzcH5-eGxnUWc2d2tXQUZmSVFBQUFBJCQAAAAAAAAAAAEAAACzakto1No5NzIyMzcxNzcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACTL2V4ky9leVl; BAIDUID=CCA70481E4D8C3CD4A58687182488276:FG=1; PSTM=1593166324; delPer=0; BCLID=7697607629013010444; BDSFRCVID=FqtOJeC62Zm2_d6uU2pKJFDzohEA-XvTH6ao92lK27TX3LzL6HHKEG0Pjx8g0KAbzQ7kogKKL2OTHmkF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tbkD_C-MfIvhDRTvhCcjh-FSMgTBKI62aKDs3Mcn-hcqEpO9QTbr3l4p5JrUKxn8K55HWRvnWIQNVfP4h-rTDUThDN0qt60qtnusQbnq-JkVf-op-PoKq4C85MoKb-LXKKOLVbFE3p7keqOYhRoI2R-R0loAq4F8WecRbfoHWhk2eno2y5jsyTkX3nPDQbQMLaQW3lokyl5psIJMhnAWbT8U5f5f--5XaKviah4-BMb1DJvDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTD-Dhe6byDGLet50sb5vfstTVatnEHJrTq4bohjPPy-R9BtQm2Co03tjxL-ohOfbO3f6PQbImhtRvqPTNQg-qBpv_QlRjjlnd5p-WyjLF2G5j0x-jLN7hVn0MW-KVOpDxj4nJyUPTD4nnBPrW3H8HL4nv2JcJbM5m3x6qLTKkQN3T-PKO5bRh_CF5tK_ahI0menJb5IC-MfTOa4oX5-o2WbCQ5KnP8pcNLPr_MtDL0bbH-l3eWCoZKqb4LJ5voKnF0lO1j4kUMRor5-T72TvgVpIa04FKqh5jDh36b6ksD-RtexnCtncy0hvcBIocShnzMUjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2b6QhDN0qt60qtnusQbnq-JkVf-op-PoKq4C85MoKb-LXKKOLVh3x0l7keqOYhRoV0J_djqonQ-JmWecRXf7HWhk2enc2y5jsyPAQQgcU5bkOXa8J3lTs04OpsIJMhnAWbT8U5f5f--5XaKviah4-BMb1DJvDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTD-Dhe6j0DGuHtj_tf5vfL5rH5P5jjtbwq4b_eUKL5-nZKxtqtHQLof7eJt5lh4JoyxjU244JQtLLXn5nWncKWKI-apkKMUbyDUv0X5Kny-R405OT2j-O0KJc0Ro0VD3chPJvyU7XXnO724nlXbrtXp7_2J0WStbKy4oTjxL1Db3JKjvMtgDtVJO-KKCBhD8m3D; H_PS_PSSID=1450_31325_32139_31254_32045_32230_31322_32256; PSINO=3; ZD_ENTRY=empty; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1594732850; REALTIME_TRANS_SWITCH=1; HISTORY_SWITCH=1; FANYI_WORD_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_afd111fa62852d1f37001d1f980b6800=1594732858; Hm_lpvt_afd111fa62852d1f37001d1f980b6800=1594776845; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1594776845; yjs_js_security_passport=b8638c6047173d1c94b5cc6d1cfe6f5b3ae96347_1594776850_js'}

    def get_input_lau(self, input_str):
        url = 'https://fanyi.baidu.com/langdetect'
        data = {
            "query": input_str
        }
        lau_arr = requests.post(url, data=data, headers=self.header)
        return lau_arr.json()

    def parse_url(self, url, input_str, from_lau, to_lau='en'):
        data = {
            "query": input_str,
            "from": from_lau,
            "to": to_lau,
            "token": self.token,
            "sign": get_sign(input_str)
        }
        response = requests.post(url, data=data, headers=self.header, cookies=self.cookies)
        return response.json()

    def run(self):
        form_lau = self.get_input_lau(self.input_str)
        if form_lau['lan'] == 'zh':
            r = self.parse_url(self.url, self.input_str, from_lau=form_lau['lan'])
        else:
            r = self.parse_url(self.url, self.input_str, from_lau=form_lau['lan'],to_lau='zh')

        print('翻译结果:', r['trans'][0]['dst'])


if __name__ == '__main__':
    text = input('请输入')
    baidu_translate = BaiduTranslate(text)
    baidu_translate.run()
# query: why are you good
# from: zh
# to: en
# token: ce90b7b40d6f5ecb81e8c7d1fc2d4397
# sign: 807951.571198

