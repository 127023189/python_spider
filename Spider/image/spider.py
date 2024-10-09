import multiprocessing

import requests
from lxml import etree
from multiprocessing import Process
import os

# PROXY_POOL_URL = 'http://localhost:5555/random'
# proxies_url = requests.get(PROXY_POOL_URL).text
#
# proxies = {
#     'http': proxies_url
# }

url = 'https://com.okmzt.net/'

header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }
def get_url(url):

    response = requests.get(url, headers=header)
    print(response)
    tree = etree.HTML(response.text)
    url = tree.xpath('//li/div/div/a[@class="uk-inline u-thumb-h"]/@href')

    return url


def download(url):
    response = requests.get(url, headers=header)
    tree = etree.HTML(response.text)
    total = tree.xpath('//div/div/main/article/progress[@class="uk-progress uk-margin-remove"]/@max')[0]
    title = tree.xpath('//div/div/main/article/h1/text()')
    image_list= []

    image = tree.xpath('//div/div/main/article/figure/img/@src')
    image_list.append(image)

    download_Pic(title[0], image_list)

def download_Pic(title, image_list):
    os.mkdir(title)
    j = 1  # 下载图片
    for item in image_list:
        filename = '%s/%s.jpg' % (title, str(j))
        print('downloading....%s : NO.%s' % (title, str(j)))
        with open(filename, 'wb') as f:
            print(item[0])
            img = requests.get(item[0], headers=header).content
            f.write(img)
        j += 1


urls = get_url(url)
def down_all_image(urls):
    worker = len(urls)
    pool = multiprocessing.Pool(processes=worker)
    print(worker)
    for url in urls:
        pool.apply_async(download,args=(url,))

    pool.close()
    pool.join()

down_all_image(urls)