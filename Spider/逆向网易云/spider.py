from functools import partial  # 锁定参数
import subprocess

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs
import requests

url = "https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token";

data = {"csrf_token": "", "encodeType": "aac", "ids": "[86369]", "level": "standard", }

# 把参数进行加密，得到密文，发请求
f = open("../wangyiyun.js", mode="r", encoding="utf-8")
js_code = f.read()
f.close()
js = execjs.compile(js_code)
mi = js.call("fn", data)
print(mi)

header ={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

resp = requests.post(url,data={"params": mi['encText'], "encSecKey": mi['encSecKey']}, headers=header)

song_url = resp.json()['data'][0]['url']
print(song_url)

song_resp = requests.get(song_url, headers=header)
with open("偏爱.m4a", mode="wb") as f:
    f.write(song_resp.content)