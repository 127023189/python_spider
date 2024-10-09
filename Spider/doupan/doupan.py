import time
from concurrent.futures import ThreadPoolExecutor
import requests
import re
import threading

url = "https://movie.douban.com/top250?start={}&filter="
header={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

obj =re.compile(r'<div class="item">.*?<span class="title">(?P<name>.*?)</span>.*?<p '+
                r'class="">.*?导演: (?P<dao>.*?)&nbsp;.*?<br>' +
                r'(?P<year>.*?)&nbsp;.*?<span class="rating_num" property="v:average">(?P<score>.*?)</span>.*?'+
                '<span>(?P<num>.*?)人评价</span>',re.S)

lock = threading.Lock()
f = open('doupan.txt','w',encoding='utf-8')

start = time.time()
def main(url):
        print(url)
        resp = requests.get(url, headers=header,timeout=10)
        print(f"resp {resp}")
        pageSource = resp.text
        result = obj.finditer(pageSource)

        for item in result:
            name = item.group('name')
            dao = item.group('dao')
            year = item.group('year').strip()
            score = item.group('score')
            num = item.group('num')
            f.write(f"{name}\t{dao}\t{year}\t{score}\t{num}\n")


l1 = []

with ThreadPoolExecutor(max_workers=10) as executor:
    for i in range(0,250,25):
        # print(url.format(i))
        executor.submit(main,url=url.format(i))
    executor.shutdown(wait=True)
end = time.time()
print(end-start)
# time.sleep(1)
# time.sleep(10)
f.close()