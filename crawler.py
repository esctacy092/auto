#!/usr/bin/env python

import os
import re
import sys

#import requests
import youtube_dl
#from lxml import etree
from loguru import logger
#from dynaconf import Dynaconf

#settings = Dynaconf(settings_files=['settings.toml'])
# logger.add("logs/stdout.log", format="{time:MM-DD HH:mm:ss} {level} {message}")

# headers = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
# }


def get_mp4(urls):
    #  https://github.com/ytdl-org/youtube-dl/blob/master/README.md#output-template
    ydl_opts = {'ignoreerrors': True, 'outtmpl': 'mp4/%(extractor)s-%(id)s-%(title)s.%(ext)s'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)


def run():
    urls = [sys.argv[1]]
    get_mp4(urls)
    logger.info("finish !")


if __name__ == "__main__":
    run()
