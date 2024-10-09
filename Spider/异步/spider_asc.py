import asyncio
import time

import aiohttp
import lxml.etree as etree
from multiprocessing import Process

header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

async def download():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://www.baidu.com", headers=header) as resp:
            html = await resp.text()
            print(html)

def main():
    loop = asyncio.get_event_loop()
    task = loop.create_task((download()))
    loop.run_until_complete(task)
    # loop.close()



if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(end-start)