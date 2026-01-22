#!/usr/bin/env python

import os
import re

#import requests
import youtube_dl
#from lxml import etree
from loguru import logger
#from dynaconf import Dynaconf

#settings = Dynaconf(settings_files=['settings.toml'])
logger.add("logs/stdout.log", format="{time:MM-DD HH:mm:ss} {level} {message}")

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
}

proxies = {
    "http": settings.proxy_url,
    "https": settings.proxy_url,
}


def get_webm(url):
    logger.info("crawling : %s" % url)
    resp = requests.get(url, headers=headers, proxies=proxies, verify=False)
    html = etree.HTML(resp.text)

    buff = '//*[@id="moreData"]//*[@class="phimage"]/a/'
    names = html.xpath(f"{buff}@href")
    urls = html.xpath(f"{buff}img/@data-mediabook")
    for i in range(len(urls)):
        try:
            url = urls[i]
            name = re.findall(r"=ph(\w+)", names[i])[-1]
            #  logger.info(f"{url} {name}")
            download(url, name, "webm")
        except Exception as err:
            logger.error(err)


def download(url, name, filetype):
    logger.debug(f"{url} {name} {filetype}")
    filepath = "%s/%s.%s" % (filetype, name, filetype)
    if os.path.exists(filepath):
        logger.info("this file had been downloaded :: %s" % filepath)
        return
    else:
        rep = requests.get(url, headers=headers, proxies=proxies)
        with open(filepath, 'wb') as file:
            file.write(rep.content)

        # urllib.request.urlretrieve(url, '%s' % filepath)
        logger.info("download success :: %s" % filepath)


def get_mp4(urls):
    #  https://github.com/ytdl-org/youtube-dl/blob/master/README.md#output-template
    ydl_opts = {'ignoreerrors': True, 'outtmpl': 'mp4/%(extractor)s-%(id)s-%(title)s.%(ext)s', 'proxy': settings.proxy_url}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)


def run(_arg=None):
    urls = [f"https://www.pornhub.com/view_video.php?viewkey={arg}"]
    get_mp4(urls)
    logger.info("finish !")


if __name__ == "__main__":
    run
