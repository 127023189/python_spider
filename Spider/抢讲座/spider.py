import random
from datetime import datetime, timedelta
import time
import requests
import re

def dataenc(e, ktimes): # 加密
    t = ktimes % 10
    if t == 0:
        t = 1
    i = []
    for a in range(len(e)):
        n = ord(e[a]) ^ t
        i.append(chr(n))
    return ''.join(i)


def getJqnonce(s):
    pattern = r'var\s+jqnonce\s*=\s*"([^"]+)"'
    return re.search(pattern, s)


def task(start_time,ktimes,username,nickname,link):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'https://www.wjx.top/wjx/join/completemobile2.aspx',  # 防盗链
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
        'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }


    response = requests.get(link, headers=headers).text
    jqnonce = getJqnonce(response).group(1) # 拿到jqnonce
    if jqnonce:
        jqsign = dataenc(jqnonce,ktimes) # 加密

        params = {
            "shortid": link.split(".")[-2].split("/")[-1],
            "starttime": start_time,
            "submittype": "1",
            "ktimes": ktimes,
            "jqnonce": jqnonce,  ##首页获取
            "jqsign": jqsign
        }
        response = requests.post(
            'https://www.wjx.top/joinnew/processjq.ashx?',
            headers=headers,
            data={
                'submitdata': f'1${username}{"}"}2${nickname}',
            },
            params=params
        )
        print(response.text)
        return response.text[0:2]


def run_task_at(target_time, *args):
    # ktimes为随机指定一个
    print(args)
    print(f"目标时间为：{target_time}")
    while True:
        current_time = datetime.now()
        if current_time >= target_time:
            print(f"到达指定时间：{current_time}")
            response = task(str((datetime.now() - timedelta(seconds=random.random())).strftime("%Y/%m/%d %H:%M:%S")),30,*args)  # 执行指定任务,模拟提交
            print(response)
            if response == str(10): # 10 为提交成功
                break
            elif response[0] == "7":
                print("滑窗验证")
                break
            else:
                break

if __name__ == '__main__':
    target_time="2024/11/28 11:42:58"
    xingming=""
    xuehao=""
    link="https://www.wjx.cn/vm/hK9BqD8.aspx#"
    run_task_at(datetime.strptime(target_time, "%Y/%m/%d %H:%M:%S"),*[xuehao,xingming,link])