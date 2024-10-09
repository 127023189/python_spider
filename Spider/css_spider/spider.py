import os

import requests
from lxml import etree
import re
from fontTools.ttLib import TTFont
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 创建 ChromeOptions 实例
chrome_options = Options()

# 设置选项，使浏览器在脚本执行后不自动关闭
chrome_options.add_experimental_option("detach", True)


url = 'https://www.maoyan.com/board/1'

header={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Cookie":"__mta=42768922.1728290832593.1728300000759.1728302007941.7; uuid_n_v=v1; uuid=BE15C090848811EFA85DCD25C220BF0B5A579BBBC1954716B67B2DD3132A0F16; _csrf=92826b45dff7e3c25a476d2d19fa87bc67dad00022db896efb38b947e0b6cbed; _lxsdk_cuid=19266293e56c8-0ebed833b7f4e5-4c657b58-1fa400-19266293e56c8; _lxsdk=BE15C090848811EFA85DCD25C220BF0B5A579BBBC1954716B67B2DD3132A0F16; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1728290832; HMACCOUNT=F2CC6E159F690CA7; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1728302007; _lxsdk_s=19266b478c4-d95-744-a51%7C%7C9"}

response = requests.get(url, headers=header)

first_num_dir = [{'code':'uniED30','num':1},{'code':'uniEA6F','num':0},{'code':'uniF7D2','num':4}]


tree = etree.HTML(response.text)
print(response.text)
items = tree.xpath('//style[contains(text(), ".woff")]/text()')
print(items)

if items:
    woff_url = re.findall(r'url\("([^"]+\.woff)"\)', items[0])[0]

data=requests.get("https:" + woff_url,headers=header).content
with open("font.woff", "wb") as f:
    f.write(data)

if os.path.exists("font.woff"):
    pass
else:
    font = TTFont("font.woff")
    font.saveXML('font.woff'+'.xml')

