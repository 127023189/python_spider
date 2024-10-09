import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from lxml import etree
import os
import requests
import asyncio
import aiohttp

fileName = r'D:\projects\python_spider\简历'
if not os.path.exists(fileName):
    os.mkdir(fileName)

header ={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

url = 'https://sc.chinaz.com/jianli/index_{}.html'

async def download(url, title):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=header) as response:
            detail_url_text = await  response.read()
            detail_tree = etree.HTML(detail_url_text)
            download_urls = detail_tree.xpath('//div[@class="clearfix mt20 downlist"]/ul/li/a/@href')[0]
            data = requests.get(url=download_urls, headers=header).content

            filePath = fileName + '/' + title + '.rar'
            with open(filePath, "wb") as f:
                f.write(data)
                print(f"保存成功{title}")

async def request_all(new_url):
    print(new_url)
    async with aiohttp.ClientSession() as session:  # 获取session
        async with session.request('GET', new_url,headers=header) as response:
            # response = requests.get(new_url, headers=header)
            response.encoding = 'utf-8'

            tree = etree.HTML(await response.read())
            # print(response.text)
            divs = tree.xpath(r'//div[@class="main_list jl_main"]')
            for div in divs:
                detail_url = div.xpath('./div/p/a/@href')
                titles = div.xpath('./div/p/a/text()')
                print(len(detail_url),len(titles))

                for jian_url, title in zip(detail_url, titles):
                    print(title, jian_url)
                    await download(jian_url, title)


def main():
    loop = asyncio.get_event_loop()
    tasks = []
    for page in range(1, 50):
        if page == 1:
            new_url = 'https://sc.chinaz.com/jianli/index.html'
        else:
            new_url = url.format(page)

        tasks.append(request_all(new_url))

    loop.run_until_complete(asyncio.wait(tasks))



if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(end - start)
