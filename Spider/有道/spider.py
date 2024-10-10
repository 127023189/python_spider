
import execjs
import json
import requests
import time

def get_sign(curtime):

    '''
    获取sign
    :return:
    '''
    with open("../../js/youdao.js", "r", encoding="utf-8") as f:
        js = f.read()
    ctx = execjs.compile(js)
    # 获取时间戳
    sign = ctx.call("sign", curtime, "fsdsogkndfokasodnaso")
    # print(sign)
    return sign

def translate(text):
    curtime = str(int(time.time() * 1000))
    sign = get_sign(curtime)
    data = {
        "i": text,
        "from": "auto",
        "to": "",
        "useTerm": "false",
        "dictResult": "true",
        "keyid": "webfanyi",
        "sign": sign,
        "client": "fanyideskweb",
        "product": "webfanyi",
        "appVersion": "1.0.0",
        "vendor": "web",
        "pointParam": "client,mysticTime,product",
        "mysticTime": curtime,
        "keyfrom": "fanyi.web",
        "mid": "1",
        "screen": "1",
        "model": "1",
        "network": "wifi",
        "abtest": "0",
        "yduuid": "abcdefg"
    }

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://fanyi.youdao.com",
        "Pragma": "no-cache",
        "Referer": "https://fanyi.youdao.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }

    url = "https://dict.youdao.com/webtranslate"

    cookies = {
        "OUTFOX_SEARCH_USER_ID":"1735453970@2001:da8:200b:c711:f85c:8568:59e1:f257",
        "OUTFOX_SEARCH_USER_ID_NCOO":"11751691.19688403",
        "DICT_DOCTRANS_SESSION_ID":"ZjI5OTQ2ZGItMjhhZC00YTE2LWI3MzctNmI4YWJkYmRkYjY3",
        "DICT_SESS":"v2|wyBJKN-MnmgL64zMO4OMROWnfJuhHzfRzEPMpunHP4RlAhMUG6LPB0km0LJy64UG0lA6LpynfJBRYWP4YGhLgK0pBnMPFh4wz0",
        "DICT_LOGIN":"1||1728542340472",
        "DICT_UT":"uqqUID_947671DCA3C6ED3DCA3E9F51765C021C"
    }

    response = requests.post(url, data=data, headers=headers,cookies=cookies)
    return decodeData(response.text)


def load_js():
    with open('../../js/youdao.js', 'r', encoding='utf-8') as f:
        return f.read()

# 解密
def decodeData(result):
    js = load_js()
    t, o = 'ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl', 'ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4'

    js_data = execjs.compile(js).call("decodeData", result, t,o)
    result = json.loads(js_data)
    print(result['translateResult'][0][0]['tgt'])





hello = translate('hello')