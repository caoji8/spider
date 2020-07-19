import requests
from retrying import retry

# verify =false 不验证ssl
# timeout 请求超时时间
# dict_form_cookie cookie转dict


headers = {}


@retry(stop_max_attempt_number=3)
def _parse_url(url,method,data,proxies):
    if method == 'POST':
        response = requests.post(url, headers=headers, timeout=3,data=data,proxies=proxies)
    else:
        response = requests.get(url, headers=headers, timeout=3,proxies=proxies)
    assert response.status_code == 200
    return response.content.decode()


def parse_url(url,method='GET',data=None,proxies={}):
    try:
        html_str = _parse_url(url,method,data,proxies)

    except:
        html_str = None
